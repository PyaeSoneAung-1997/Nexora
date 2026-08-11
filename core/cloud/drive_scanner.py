import threading
from googleapiclient.discovery import build
from core.cloud.auth_manager import GoogleAuthManager
from core.database.db_manager import DatabaseManager


class DriveScanner:
    """Drive Location (Home, My Drive, Shared Drives, Specific Folders) အလိုက် Scan ဖတ်ပေးမည့် Engine"""

    def __init__(self, auth_manager: GoogleAuthManager = None, db_manager: DatabaseManager = None):
        self.auth_mgr = auth_manager or GoogleAuthManager()
        self.db = db_manager or DatabaseManager()

    def get_drive_service(self, account_id: int):
        creds = self.auth_mgr.get_credentials(account_id)
        if not creds:
            raise ValueError(f"No active credentials for Account ID: {account_id}")
        return build("drive", "v3", credentials=creds)

    def list_shared_drives(self, account_id: int) -> list[dict]:
        """User လက်လှမ်းမီသော Shared Drives အားလုံးကို List ထုတ်ပေးမည်"""
        service = self.get_drive_service(account_id)
        shared_drives = []
        page_token = None

        while True:
            response = service.drives().list(
                pageSize=100,
                pageToken=page_token,
                fields="nextPageToken, drives(id, name)"
            ).execute()

            for sd in response.get("drives", []):
                shared_drives.append({
                    "id": sd["id"],
                    "name": sd["name"],
                    "type": "shared_drive"
                })

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return shared_drives

    def _register_drive(self, account_id: int, drive_id: str, name: str, drive_type: str):
        """drives table ထဲ Drive အချက်အလက် ကြိုတင် သွင်းမည်"""
        query = """
            INSERT INTO drives (account_id, drive_id, name, type, last_scanned, status)
            VALUES (?, ?, ?, ?, datetime('now', 'localtime'), 'scanning')
            ON CONFLICT(drive_id) DO UPDATE SET
                name = excluded.name,
                type = excluded.type,
                last_scanned = datetime('now', 'localtime'),
                status = 'scanning';
        """
        self.db.execute_query(query, (account_id, drive_id, name, drive_type))

    def scan_my_drive(
        self, account_id: int, job_id: int = None, 
        pause_event: threading.Event = None, stop_event: threading.Event = None
    ) -> dict:
        """My Drive တစ်ခုတည်းရှိ ဖိုင်/ဖိုဒါ အားလုံးကို Scan ဖတ်မည်"""
        service = self.get_drive_service(account_id)
        self._register_drive(account_id, drive_id="root", name="My Drive", drive_type="my_drive")
        query = "'me' in owners and trashed = false"
        
        return self._fetch_and_save_files(
            service, account_id, drive_id="root", query=query, corpora="user",
            job_id=job_id, pause_event=pause_event, stop_event=stop_event
        )

    def scan_single_shared_drive(
        self, account_id: int, shared_drive_id: str, shared_drive_name: str,
        job_id: int = None, pause_event: threading.Event = None, stop_event: threading.Event = None
    ) -> dict:
        """ရွေးချယ်လိုက်သော Shared Drive တစ်ခုကို Scan ဖတ်မည်"""
        # Guard: shared_drive_id နေရာတွင် "root" ရောက်လာပါက My Drive သို့ လမ်းကြောင်းလွှဲပေးခြင်း
        if not shared_drive_id or shared_drive_id.lower() == "root":
            print("⚠️ 'root' သည် Shared Drive ID မဟုတ်ပါ။ My Drive Scan သို့ လွှဲပြောင်းပေးလိုက်ပါသည်။")
            return self.scan_my_drive(account_id, job_id=job_id, pause_event=pause_event, stop_event=stop_event)

        service = self.get_drive_service(account_id)
        self._register_drive(account_id, drive_id=shared_drive_id, name=shared_drive_name, drive_type="shared_drive")

        query = "trashed = false"
        return self._fetch_and_save_files(
            service, account_id, drive_id=shared_drive_id, query=query,
            corpora="drive", shared_drive_id=shared_drive_id,
            job_id=job_id, pause_event=pause_event, stop_event=stop_event
        )

    def scan_folder(
        self, account_id: int, folder_id: str, folder_name: str = "Folder Scan",
        job_id: int = None, pause_event: threading.Event = None, stop_event: threading.Event = None
    ) -> dict:
        """သတ်မှတ်ထားသော Folder ID တစ်ခုအောက်ရှိ ဖိုင်/ဖိုဒါများကို Scan ဖတ်မည်"""
        service = self.get_drive_service(account_id)
        self._register_drive(account_id, drive_id=folder_id, name=folder_name, drive_type="folder")

        query = f"'{folder_id}' in parents and trashed = false"
        return self._fetch_and_save_files(
            service, account_id, drive_id=folder_id, query=query,
            corpora="allDrives", job_id=job_id, pause_event=pause_event, stop_event=stop_event
        )

    def _fetch_and_save_files(
        self, service, account_id: int, drive_id: str, query: str, corpora: str, 
        shared_drive_id: str = None, job_id: int = None,
        pause_event: threading.Event = None, stop_event: threading.Event = None
    ) -> dict:
        
        if not job_id:
            job_query = """
                INSERT INTO sync_jobs (account_id, drive_id, job_type, status, started_at, updated_at)
                VALUES (?, ?, 'scan', 'running', datetime('now', 'localtime'), datetime('now', 'localtime'))
            """
            job_id = self.db.execute_query(job_query, (account_id, drive_id))
            page_token = None
            scanned_files = 0
            scanned_folders = 0
        else:
            job = self.db.fetch_one("SELECT next_page_token, scanned_files, scanned_folders FROM sync_jobs WHERE id = ?", (job_id,))
            page_token = job["next_page_token"] if job else None
            scanned_files = job["scanned_files"] if job else 0
            scanned_folders = job["scanned_folders"] if job else 0
            self.db.execute_query("UPDATE sync_jobs SET status = 'running', updated_at = datetime('now', 'localtime') WHERE id = ?", (job_id,))

        params = {
            "q": query,
            "pageSize": 200,
            "fields": "nextPageToken, files(id, name, mimeType, size, parents, webViewLink, md5Checksum, trashed, createdTime, modifiedTime)",
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True
        }

        if corpora == "drive" and shared_drive_id and shared_drive_id.lower() != "root":
            params["corpora"] = "drive"
            params["driveId"] = shared_drive_id
        elif corpora == "allDrives":
            params["corpora"] = "allDrives"
        else:
            params["corpora"] = "user"

        try:
            while True:
                if pause_event:
                    pause_event.wait()

                if stop_event and stop_event.is_set():
                    self.db.execute_query("""
                        UPDATE sync_jobs SET status = 'cancelled', updated_at = datetime('now', 'localtime') WHERE id = ?
                    """, (job_id,))
                    self.db.execute_query("UPDATE drives SET status = 'idle' WHERE drive_id = ?", (drive_id,))
                    return {"status": "cancelled", "job_id": job_id, "scanned_files": scanned_files, "scanned_folders": scanned_folders}

                params["pageToken"] = page_token
                response = service.files().list(**params).execute()
                files = response.get("files", [])

                file_records = []
                for f in files:
                    mime_type = f.get("mimeType", "")
                    is_folder = 1 if mime_type == "application/vnd.google-apps.folder" else 0
                    is_workspace = 1 if (mime_type.startswith("application/vnd.google-apps.") and not is_folder) else 0

                    if is_folder:
                        scanned_folders += 1
                    else:
                        scanned_files += 1

                    parent = f.get("parents", [None])[0]
                    created_at = f.get("createdTime")
                    modified_time = f.get("modifiedTime")

                    file_records.append((
                        account_id, drive_id, f["id"], parent, f["name"], mime_type,
                        int(f.get("size", 0)), is_folder, is_workspace, f["name"],
                        f.get("md5Checksum"), f.get("webViewLink"), 1 if f.get("trashed") else 0,
                        created_at, modified_time
                    ))

                if file_records:
                    save_query = """
                        INSERT INTO drive_files (
                            account_id, drive_id, file_id, parent_id, name, mime_type, size,
                            is_folder, is_workspace_file, relative_path, md5_checksum, web_view_link,
                            trashed, created_at, modified_time, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
                        ON CONFLICT(file_id) DO UPDATE SET
                            account_id = excluded.account_id,
                            drive_id = excluded.drive_id,
                            parent_id = excluded.parent_id,
                            name = excluded.name,
                            mime_type = excluded.mime_type,
                            size = excluded.size,
                            is_folder = excluded.is_folder,
                            is_workspace_file = excluded.is_workspace_file,
                            relative_path = excluded.relative_path,
                            md5_checksum = excluded.md5_checksum,
                            web_view_link = excluded.web_view_link,
                            trashed = excluded.trashed,
                            modified_time = excluded.modified_time,
                            updated_at = datetime('now', 'localtime');
                    """
                    self.db.execute_many(save_query, file_records)

                page_token = response.get("nextPageToken")

                self.db.execute_query("""
                    UPDATE sync_jobs SET 
                        next_page_token = ?, scanned_files = ?, scanned_folders = ?, updated_at = datetime('now', 'localtime')
                    WHERE id = ?
                """, (page_token, scanned_files, scanned_folders, job_id))

                if not page_token:
                    break

            self.db.execute_query("""
                UPDATE drives SET
                    total_files = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
                    total_folders = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 1 AND trashed = 0),
                    total_size = (SELECT COALESCE(SUM(size), 0) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
                    status = 'idle',
                    last_scanned = datetime('now', 'localtime')
                WHERE drive_id = ?;
            """, (drive_id, drive_id, drive_id, drive_id))

            self.db.execute_query("""
                UPDATE sync_jobs SET
                    status = 'completed',
                    completed_at = datetime('now', 'localtime'),
                    updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (job_id,))

            return {"job_id": job_id, "scanned_files": scanned_files, "scanned_folders": scanned_folders}

        except Exception as e:
            self.db.execute_query("""
                UPDATE sync_jobs SET
                    status = 'failed',
                    error_message = ?,
                    updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (str(e), job_id))

            self.db.execute_query("UPDATE drives SET status = 'failed' WHERE drive_id = ?", (drive_id,))
            raise e