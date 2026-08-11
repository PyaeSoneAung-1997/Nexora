# core/cloud/drive_scanner.py

import threading
from googleapiclient.discovery import build
from core.cloud.auth_manager import GoogleAuthManager
from core.database.db_manager import DatabaseManager


class DriveScanner:
    """Drive Location (Home, My Drive, Shared Drives) အလိုက် DB Schema အတိအကျဖြင့် Scan ဖတ်ပေးမည့် Engine"""

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

    # def scan_my_drive(self, account_id: int) -> dict:
    #     """My Drive တစ်ခုတည်းရှိ ဖိုင်/ဖိုဒါ အားလုံးကို Scan ဖတ်မည်"""
    #     service = self.get_drive_service(account_id)
    #     print("🔍 Scanning My Drive...")

    #     self._register_drive(account_id, drive_id="root", name="My Drive", drive_type="my_drive")
    #     query = "'me' in owners and trashed = false"
    #     scanned_info = self._fetch_and_save_files(service, account_id, drive_id="root", query=query, corpora="user")

    #     return {"drive_id": "root", "name": "My Drive", **scanned_info}

    def scan_single_shared_drive(
            self, account_id: int, shared_drive_id: str, shared_drive_name: str,
            job_id: int = None, pause_event: threading.Event = None, stop_event: threading.Event = None
        ) -> dict:
            """ရွေးချယ်လိုက်သော Shared Drive တစ်ခုကို Scan ဖတ်မည်"""
            service = self.get_drive_service(account_id)
            print(f"🔍 Scanning Shared Drive: {shared_drive_name} ({shared_drive_id})...")
    
            self._register_drive(account_id, drive_id=shared_drive_id, name=shared_drive_name, drive_type="shared_drive")
    
            query = "trashed = false"
            return self._fetch_and_save_files(
                service, account_id, drive_id=shared_drive_id, query=query,
                corpora="drive", shared_drive_id=shared_drive_id,
                job_id=job_id, pause_event=pause_event, stop_event=stop_event
            )
    
    # def process_location(
    #     self,
    #     account_id: int,
    #     location: str,
    #     home_option: str = None,
    #     selected_shared_drive_ids: list[str] = None
    # ):
    #     """
    #     Location Route အလိုက် အလိုအလျောက် ခွဲခြား လုပ်ဆောင်ပေးမည့် Main Function
    #     """
    #     loc = location.lower().strip().replace("/", "\\")

    #     # CASE 1: drive\home
    #     if loc == "drive\\home":
    #         if not home_option:
    #             return {
    #                 "type": "home_option_required",
    #                 "options": [
    #                     {"id": "my_drive", "label": "My Drive Only"},
    #                     {"id": "shared_drives", "label": "Shared Drives"},
    #                     {"id": "all", "label": "My Drive + Shared Drives (All)"}
    #                 ]
    #             }

    #         if home_option == "my_drive":
    #             return {"type": "home", "selected": "my_drive", "result": self.scan_my_drive(account_id)}

    #         elif home_option == "shared_drives":
    #             all_sds = self.list_shared_drives(account_id)
    #             if not selected_shared_drive_ids:
    #                 return {
    #                     "type": "shared_drives_selection_required",
    #                     "available_shared_drives": all_sds
    #                 }
    #             sd_results = [
    #                 self.scan_single_shared_drive(account_id, sd["id"], sd["name"])
    #                 for sd in all_sds if sd["id"] in selected_shared_drive_ids
    #             ]
    #             return {"type": "home", "selected": "shared_drives", "scanned": sd_results}

    #         elif home_option == "all":
    #             res_my_drive = self.scan_my_drive(account_id)
    #             all_sds = self.list_shared_drives(account_id)
    #             sd_results = [
    #                 self.scan_single_shared_drive(account_id, sd["id"], sd["name"])
    #                 for sd in all_sds
    #             ]
    #             return {
    #                 "type": "home",
    #                 "selected": "all",
    #                 "my_drive": res_my_drive,
    #                 "shared_drives": sd_results
    #             }

    #     # CASE 2: drive\my-drive
    #     elif loc == "drive\\my-drive":
    #         return {"type": "my_drive", "result": self.scan_my_drive(account_id)}

    #     # CASE 3: drive\shared-drives
    #     elif loc == "drive\\shared-drives":
    #         all_sds = self.list_shared_drives(account_id)

    #         if not selected_shared_drive_ids:
    #             return {
    #                 "type": "shared_drives_selection_required",
    #                 "available_shared_drives": all_sds
    #             }

    #         sd_results = [
    #             self.scan_single_shared_drive(account_id, sd["id"], sd["name"])
    #             for sd in all_sds if sd["id"] in selected_shared_drive_ids
    #         ]
    #         return {"type": "shared_drives", "scanned": sd_results}

    #     else:
    #         raise ValueError(f"Unknown location: {location}")

    # def _register_drive(self, account_id: int, drive_id: str, name: str, drive_type: str) -> int:
    #     """drives table ထဲ Drive အချက်အလက် သွင်းမည်"""
    #     query = """
    #         INSERT INTO drives (account_id, drive_id, name, type, last_scanned, status)
    #         VALUES (?, ?, ?, ?, datetime('now', 'localtime'), 'scanning')
    #         ON CONFLICT(drive_id) DO UPDATE SET
    #             name = excluded.name,
    #             type = excluded.type,
    #             last_scanned = datetime('now', 'localtime'),
    #             status = 'scanning';
    #     """
    #     return self.db.execute_query(query, (account_id, drive_id, name, drive_type))

    def _fetch_and_save_files(self, service, account_id: int, drive_id: str, query: str, corpora: str, shared_drive_id: str = None) -> dict:
        # 1. Sync Job တစ်ခု စတင်ပြီး DB သို့ သွင်းမည်
        job_query = """
            INSERT INTO sync_jobs (account_id, drive_id, job_type, status, started_at, updated_at)
            VALUES (?, ?, 'scan', 'running', datetime('now', 'localtime'), datetime('now', 'localtime'))
        """
        job_id = self.db.execute_query(job_query, (account_id, drive_id))

        page_token = None
        scanned_files = 0
        scanned_folders = 0

        params = {
            "q": query,
            "pageSize": 500,
            "fields": "nextPageToken, files(id, name, mimeType, size, parents, webViewLink, md5Checksum, trashed, createdTime, modifiedTime)",
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True
        }

        if corpora == "drive" and shared_drive_id:
            params["corpora"] = "drive"
            params["driveId"] = shared_drive_id
        else:
            params["corpora"] = "user"

        try:
            while True:
                params["pageToken"] = page_token
                response = service.files().list(**params).execute()
                files = response.get("files", [])

                for f in files:
                    mime_type = f.get("mimeType", "")
                    is_folder = 1 if mime_type == "application/vnd.google-apps.folder" else 0
                    is_workspace = 1 if (mime_type.startswith("application/vnd.google-apps.") and not is_folder) else 0

                    if is_folder:
                        scanned_folders += 1
                    else:
                        scanned_files += 1

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
                    parent = f.get("parents", [None])[0]
                    created_at = f.get("createdTime")
                    modified_time = f.get("modifiedTime")

                    self.db.execute_query(save_query, (
                        account_id, drive_id, f["id"], parent, f["name"], mime_type,
                        int(f.get("size", 0)), is_folder, is_workspace, f["name"],
                        f.get("md5Checksum"), f.get("webViewLink"), 1 if f.get("trashed") else 0,
                        created_at, modified_time
                    ))

                page_token = response.get("nextPageToken")
                
                # Progress ကို sync_jobs ထဲ Update လုပ်မည်
                self.db.execute_query("""
                    UPDATE sync_jobs SET 
                        next_page_token = ?, scanned_files = ?, scanned_folders = ?, updated_at = datetime('now', 'localtime')
                    WHERE id = ?
                """, (page_token, scanned_files, scanned_folders, job_id))

                if not page_token:
                    break

            # 2. drives table ထဲရှိ total_files, total_folders, total_size များကို DB Aggregate Query ဖြင့် Update ပြုလုပ်မည်
            self.db.execute_query("""
                UPDATE drives SET
                    total_files = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
                    total_folders = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 1 AND trashed = 0),
                    total_size = (SELECT COALESCE(SUM(size), 0) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
                    status = 'idle',
                    last_scanned = datetime('now', 'localtime')
                WHERE drive_id = ?;
            """, (drive_id, drive_id, drive_id, drive_id))

            # 3. sync_jobs ကို Completed အဖြစ် သတ်မှတ်မည်
            self.db.execute_query("""
                UPDATE sync_jobs SET
                    status = 'completed',
                    completed_at = datetime('now', 'localtime'),
                    updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (job_id,))

            return {"scanned_files": scanned_files, "scanned_folders": scanned_folders}

        except Exception as e:
            # Error တက်ပါက sync_jobs နှင့် drives တန်ဖိုးများကို failed သို့ ပြောင်းမည်
            self.db.execute_query("""
                UPDATE sync_jobs SET
                    status = 'failed',
                    error_message = ?,
                    updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (str(e), job_id))

            self.db.execute_query("UPDATE drives SET status = 'failed' WHERE drive_id = ?", (drive_id,))
            raise e