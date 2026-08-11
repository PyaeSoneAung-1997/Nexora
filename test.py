# # import re
# # from googleapiclient.discovery import build
# # from googleapiclient.errors import HttpError
# # from core.cloud.auth_manager import GoogleAuthManager
# # from core.database.db_manager import DatabaseManager

# # class DriveResolver:
# #     """Google Drive Link/ID များကို စစ်ဆေးပြီး Metadata ထုတ်ယူကာ DB သို့ သိမ်းဆည်းပေးမည့် Service"""

# #     def __init__(self, auth_manager: GoogleAuthManager = None, db_manager: DatabaseManager = None):
# #         self.auth_mgr = auth_manager or GoogleAuthManager()
# #         self.db = db_manager or DatabaseManager()

# #     @staticmethod
# #     def extract_id(url_or_id: str) -> str | None:
# #             """Google Drive URL သို့မဟုတ် Raw ID ထဲမှ Target ID ကို သီးသန့် ထုတ်ယူမည်"""
# #             if not url_or_id:
# #                 return None

# #             url_or_id = url_or_id.strip()

# #             # 1. Folder Link စစ်မည် (/folders/xxx)
# #             folder_match = re.search(r"/folders/([\w-]+)", url_or_id)
# #             if folder_match:
# #                 return folder_match.group(1)

# #             # 2. File Link စစ်မည် (/file/d/xxx)
# #             file_match = re.search(r"/file/d/([\w-]+)", url_or_id)
# #             if file_match:
# #                 return file_match.group(1)

# #             # 3. ID = parameter ပါသော Link (e.g., open?id=xxx)
# #             id_param_match = re.search(r"[?&]id=([\w-]+)", url_or_id)
# #             if id_param_match:
# #                 return id_param_match.group(1)

# #             # 4. Raw ID သီးသန့် ရိုက်ထည့်ထားခြင်း (အနည်းဆုံး ၂၅ လုံးနှင့်အထက်)
# #             if re.fullmatch(r"[\w-]{25,}", url_or_id):
# #                 return url_or_id

# #             return None

# #     # def resolve(self, account_id: int, url_or_id: str, save_to_db: bool = True) -> dict:
# #     def resolve(self, account_id: int, url_or_id: str) -> dict:
# #             """
# #             Drive ID ကို API ခေါ်ပြီး File/Folder Metadata အချက်အလက်များ တောင်းယူမည်။
# #             `save_to_db=True` ပါပါက `drive_files` Table ထဲသို့ တိုက်ရိုက် သိမ်းဆည်းပေးမည်။
# #             """
            

# #             creds = self.auth_mgr.get_credentials(account_id)
# #             if not creds:
# #                 raise ValueError(f"No active session found for Account ID: {account_id}")

# #             service = build("drive", "v3", credentials=creds)

# #             check_url = url.lower()
# #             if "/home" in check_url:
# #                 return {
# #                                         "type": "home",
# #                                         "action":"all_drives",
            
# #                                         "id": None,
# #                                         "name": "Drive Home",
            
# #                                         "drive_type":None,
# #                                         "drive_id": None,
            
# #                                         "mime_type": None,
# #                                         "is_folder": 0
# #                                     }
# #             if "/my-drive" in check_url or "my_drive" in check_url:
# #                                 return {
# #                                                 "type": "home",
# #                                                 "action":"all_drives",
                        
# #                                                 "id": None,
# #                                                 "name": "Drive Home",
                        
# #                                                 "drive_type":None,
# #                                                 "drive_id": None,
                        
# #                                                 "mime_type": None,
# #                                                 "is_folder": 0
# #                                         }     
# #             if "/shared-drives"  in check_url:
# #                             return {
# #                                               "type": "home",
# #                                               "action":"all_drives",
                      
# #                                               "id": None,
# #                                               "name": "Drive Home",
                      
# #                                               "drive_type":None,
# #                                               "drive_id": None,
                      
# #                                               "mime_type": None,
# #                                               "is_folder": 0
# #                                     }     

# #                       # Google Drive API မှတစ်ဆင့် Metadata တောင်းယူမည်
# #             target_id = self.extract_id(url_or_id)
# #             if not target_id:
# #                     raise ValueError("Invalid Google Drive Link or ID format.")
# #             try:
# #                 # Google Drive API မှတစ်ဆင့် Metadata တောင်းယူမည်
# #                 f = service.files().get(
# #                     fileId=target_id,
# #                     fields="id, name, mimeType, size, parents, driveId, webViewLink, md5Checksum, trashed, createdTime, modifiedTime",
# #                     supportsAllDrives=True
# #                 ).execute()

# #                 mime_type = f.get("mimeType", "")
# #                 is_folder = 1 if mime_type == "application/vnd.google-apps.folder" else 0
# #                 is_workspace = 1 if (mime_type.startswith("application/vnd.google-apps.") and not is_folder) else 0
# #                 parent_id = f.get("parents", [None])[0]
# #                 drive_id = f.get("driveId", "root") # Shared Drive မဟုတ်ပါက 'root' ဟု သတ်မှတ်မည်

# #                 result_data = {
# #                     "account_id": account_id,
# #                     "drive_id": drive_id,
# #                     "file_id": f["id"],
# #                     "parent_id": parent_id,
# #                     "name": f["name"],
# #                     "mime_type": mime_type,
# #                     "size": int(f.get("size", 0)),
# #                     "is_folder": is_folder,
# #                     "is_workspace_file": is_workspace,
# #                     "relative_path": f["name"],
# #                     "md5_checksum": f.get("md5Checksum"),
# #                     "web_view_link": f.get("webViewLink"),
# #                     "trashed": 1 if f.get("trashed") else 0,
# #                     "created_at": f.get("createdTime"),
# #                     "modified_time": f.get("modifiedTime")
# #                 }
# #                 return result_data
       
# #             except HttpError as e:
# #                    if e.resp.status == 404:
# #                        raise FileNotFoundError("Drive item not found or permission denied.")
# #                    raise Exception(f"Google Drive API Error: {e.reason}")
            
# # if __name__  ==  "__main__":
# #     id = "1"
# #     url = "https://drive.google.com/drive/folders/16J1isPtoHQJIOWfbRD3rfmYh7MhTIKw6"
# #     # url = "https://drive.google.com/drive/my-drive"
# #     # url = "https://drive.google.com/drive/shared-drives"

# #     manager = DriveResolver()
# #     result = manager.resolve(id ,url)
# #     print(result)

# import threading
# from googleapiclient.discovery import build
# from core.cloud.auth_manager import GoogleAuthManager
# from core.database.db_manager import DatabaseManager


# class DriveScanner:
#     """Drive Location (Home, My Drive, Shared Drives) အလိုက် DB Schema အတိအကျဖြင့် Scan ဖတ်ပေးမည့် Engine"""

#     def __init__(self, auth_manager: GoogleAuthManager = None, db_manager: DatabaseManager = None):
#         self.auth_mgr = auth_manager or GoogleAuthManager()
#         self.db = db_manager or DatabaseManager()

#     def get_drive_service(self, account_id: int):
#         creds = self.auth_mgr.get_credentials(account_id)
#         if not creds:
#             raise ValueError(f"No active credentials for Account ID: {account_id}")
#         return build("drive", "v3", credentials=creds)

#     def list_shared_drives(self, account_id: int) -> list[dict]:
#         """User လက်လှမ်းမီသော Shared Drives အားလုံးကို List ထုတ်ပေးမည်"""
#         service = self.get_drive_service(account_id)
#         shared_drives = []
#         page_token = None

#         while True:
#             response = service.drives().list(
#                 pageSize=100,
#                 pageToken=page_token,
#                 fields="nextPageToken, drives(id, name)"
#             ).execute()

#             for sd in response.get("drives", []):
#                 shared_drives.append({
#                     "id": sd["id"],
#                     "name": sd["name"],
#                     "type": "shared_drive"
#                 })

#             page_token = response.get("nextPageToken")
#             if not page_token:
#                 break

#         return shared_drives

#     # def _register_drive(self, account_id: int, drive_id: str, name: str, drive_type: str):
#     #     """drives table ထဲ Drive အချက်အလက် ကြိုတင် သွင်းမည်"""
#     #     query = """
#     #         INSERT INTO drives (account_id, drive_id, name, type, last_scanned, status)
#     #         VALUES (?, ?, ?, ?, datetime('now', 'localtime'), 'scanning')
#     #         ON CONFLICT(drive_id) DO UPDATE SET
#     #             name = excluded.name,
#     #             type = excluded.type,
#     #             last_scanned = datetime('now', 'localtime'),
#     #             status = 'scanning';
#     #     """
#     #     self.db.execute_query(query, (account_id, drive_id, name, drive_type))

#     # def scan_my_drive(
#     #     self, account_id: int, job_id: int = None, 
#     #     pause_event: threading.Event = None, stop_event: threading.Event = None
#     # ) -> dict:
#     #     """My Drive တစ်ခုတည်းရှိ ဖိုင်/ဖိုဒါ အားလုံးကို Scan ဖတ်မည်"""
#     #     service = self.get_drive_service(account_id)
#     #     print("🔍 Scanning My Drive...")

#     #     self._register_drive(account_id, drive_id="root", name="My Drive", drive_type="my_drive")
#     #     query = "'me' in owners and trashed = false"
        
#     #     return self._fetch_and_save_files(
#     #         service, account_id, drive_id="root", query=query, corpora="user",
#     #         job_id=job_id, pause_event=pause_event, stop_event=stop_event
#     #     )

#     def scan_single_shared_drive(
#         self, account_id: int, shared_drive_id: str, shared_drive_name: str,
#         job_id: int = None, pause_event: threading.Event = None, stop_event: threading.Event = None
#     ) -> dict:
#         """ရွေးချယ်လိုက်သော Shared Drive တစ်ခုကို Scan ဖတ်မည်"""
#         service = self.get_drive_service(account_id)
#         print(f"🔍 Scanning Shared Drive: {shared_drive_name} ({shared_drive_id})...")

#         self._register_drive(account_id, drive_id=shared_drive_id, name=shared_drive_name, drive_type="shared_drive")

#         query = "trashed = false"
#         return self._fetch_and_save_files(
#             service, account_id, drive_id=shared_drive_id, query=query,
#             corpora="drive", shared_drive_id=shared_drive_id,
#             job_id=job_id, pause_event=pause_event, stop_event=stop_event
#         )

#     def _fetch_and_save_files(
#         self, service, account_id: int, drive_id: str, query: str, corpora: str, 
#         shared_drive_id: str = None, job_id: int = None,
#         pause_event: threading.Event = None, stop_event: threading.Event = None
#     ) -> dict:
        
#         # 1. Job အသစ် သို့မဟုတ် အဟောင်း Resume လုပ်ရန် စစ်ဆေးခြင်း
#         if not job_id:
#             job_query = """
#                 INSERT INTO sync_jobs (account_id, drive_id, job_type, status, started_at, updated_at)
#                 VALUES (?, ?, 'scan', 'running', datetime('now', 'localtime'), datetime('now', 'localtime'))
#             """
#             job_id = self.db.execute_query(job_query, (account_id, drive_id))
#             page_token = None
#             scanned_files = 0
#             scanned_folders = 0
#         else:
#             job = self.db.fetch_one("SELECT next_page_token, scanned_files, scanned_folders FROM sync_jobs WHERE id = ?", (job_id,))
#             page_token = job["next_page_token"] if job else None
#             scanned_files = job["scanned_files"] if job else 0
#             scanned_folders = job["scanned_folders"] if job else 0
#             self.db.execute_query("UPDATE sync_jobs SET status = 'running', updated_at = datetime('now', 'localtime') WHERE id = ?", (job_id,))

#         params = {
#             "q": query,
#             "pageSize": 200,
#             "fields": "nextPageToken, files(id, name, mimeType, size, parents, webViewLink, md5Checksum, trashed, createdTime, modifiedTime)",
#             "supportsAllDrives": True,
#             "includeItemsFromAllDrives": True
#         }

#         if corpora == "drive" and shared_drive_id:
#             params["corpora"] = "drive"
#             params["driveId"] = shared_drive_id
#         else:
#             params["corpora"] = "user"

#         try:
#             while True:
#                 # PAUSE စစ်ဆေးခြင်း
#                 if pause_event:
#                     pause_event.wait()

#                 # STOP စစ်ဆေးခြင်း
#                 if stop_event and stop_event.is_set():
#                     self.db.execute_query("""
#                         UPDATE sync_jobs SET status = 'cancelled', updated_at = datetime('now', 'localtime') WHERE id = ?
#                     """, (job_id,))
#                     self.db.execute_query("UPDATE drives SET status = 'idle' WHERE drive_id = ?", (drive_id,))
#                     return {"status": "cancelled", "job_id": job_id, "scanned_files": scanned_files, "scanned_folders": scanned_folders}

#                 params["pageToken"] = page_token
#                 response = service.files().list(**params).execute()
#                 files = response.get("files", [])

#                 file_records = []
#                 for f in files:
#                     mime_type = f.get("mimeType", "")
#                     is_folder = 1 if mime_type == "application/vnd.google-apps.folder" else 0
#                     is_workspace = 1 if (mime_type.startswith("application/vnd.google-apps.") and not is_folder) else 0

#                     if is_folder:
#                         scanned_folders += 1
#                     else:
#                         scanned_files += 1

#                     parent = f.get("parents", [None])[0]
#                     created_at = f.get("createdTime")
#                     modified_time = f.get("modifiedTime")

#                     file_records.append((
#                         account_id, drive_id, f["id"], parent, f["name"], mime_type,
#                         int(f.get("size", 0)), is_folder, is_workspace, f["name"],
#                         f.get("md5Checksum"), f.get("webViewLink"), 1 if f.get("trashed") else 0,
#                         created_at, modified_time
#                     ))

#                 # Batch Insert ပြုလုပ်ခြင်း (Query execution ပိုမြန်စေသည်)
#                 if file_records:
#                     save_query = """
#                         INSERT INTO drive_files (
#                             account_id, drive_id, file_id, parent_id, name, mime_type, size,
#                             is_folder, is_workspace_file, relative_path, md5_checksum, web_view_link,
#                             trashed, created_at, modified_time, updated_at
#                         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
#                         ON CONFLICT(file_id) DO UPDATE SET
#                             account_id = excluded.account_id,
#                             drive_id = excluded.drive_id,
#                             parent_id = excluded.parent_id,
#                             name = excluded.name,
#                             mime_type = excluded.mime_type,
#                             size = excluded.size,
#                             is_folder = excluded.is_folder,
#                             is_workspace_file = excluded.is_workspace_file,
#                             relative_path = excluded.relative_path,
#                             md5_checksum = excluded.md5_checksum,
#                             web_view_link = excluded.web_view_link,
#                             trashed = excluded.trashed,
#                             modified_time = excluded.modified_time,
#                             updated_at = datetime('now', 'localtime');
#                     """
#                     self.db.execute_many(save_query, file_records)

#                 page_token = response.get("nextPageToken")

#                 # Job Progress ကို Update မှတ်ခြင်း
#                 self.db.execute_query("""
#                     UPDATE sync_jobs SET 
#                         next_page_token = ?, scanned_files = ?, scanned_folders = ?, updated_at = datetime('now', 'localtime')
#                     WHERE id = ?
#                 """, (page_token, scanned_files, scanned_folders, job_id))

#                 if not page_token:
#                     break

#             # 2. Total Summary များကို Drives Table တွင် Update လုပ်ခြင်း
#             self.db.execute_query("""
#                 UPDATE drives SET
#                     total_files = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
#                     total_folders = (SELECT COUNT(*) FROM drive_files WHERE drive_id = ? AND is_folder = 1 AND trashed = 0),
#                     total_size = (SELECT COALESCE(SUM(size), 0) FROM drive_files WHERE drive_id = ? AND is_folder = 0 AND trashed = 0),
#                     status = 'idle',
#                     last_scanned = datetime('now', 'localtime')
#                 WHERE drive_id = ?;
#             """, (drive_id, drive_id, drive_id, drive_id))

#             # 3. Sync Job အခြေအနေကို Completed ပြောင်းခြင်း
#             self.db.execute_query("""
#                 UPDATE sync_jobs SET
#                     status = 'completed',
#                     completed_at = datetime('now', 'localtime'),
#                     updated_at = datetime('now', 'localtime')
#                 WHERE id = ?
#             """, (job_id,))

#             return {"job_id": job_id, "scanned_files": scanned_files, "scanned_folders": scanned_folders}

#         except Exception as e:
#             self.db.execute_query("""
#                 UPDATE sync_jobs SET
#                     status = 'failed',
#                     error_message = ?,
#                     updated_at = datetime('now', 'localtime')
#                 WHERE id = ?
#             """, (str(e), job_id))

#             self.db.execute_query("UPDATE drives SET status = 'failed' WHERE drive_id = ?", (drive_id,))
#             raise e

import tkinter as tk
from tkinter import ttk, messagebox
from core.database.db_manager import DatabaseManager
from core.sync.sync_manager import SyncManager


class SyncTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Google Drive Sync Engine - Test UI")
        self.geometry("520x380")
        self.resizable(False, False)

        # Managers
        self.db = DatabaseManager()
        self.sync_mgr = SyncManager()

        self._init_ui()
        self._start_status_polling()

    def _init_ui(self):
        # 1. Input Section
        input_frame = ttk.LabelFrame(self, text=" Sync Settings ")
        input_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(input_frame, text="Account ID:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.ent_account_id = ttk.Entry(input_frame, width=15)
        self.ent_account_id.insert(0, "1")
        self.ent_account_id.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(input_frame, text="Drive ID:").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        self.ent_drive_id = ttk.Entry(input_frame, width=20)
        self.ent_drive_id.insert(0, "root")  # "root" = My Drive
        self.ent_drive_id.grid(row=0, column=3, padx=10, pady=8)

        # 2. Control Buttons Section
        btn_frame = ttk.LabelFrame(self, text=" Controls ")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ttk.Button(btn_frame, text="▶️ Start", command=self.start_sync).grid(row=0, column=0, padx=8, pady=10)
        ttk.Button(btn_frame, text="⏸️ Pause", command=self.pause_sync).grid(row=0, column=1, padx=8, pady=10)
        ttk.Button(btn_frame, text="⏯️ Resume", command=self.resume_sync).grid(row=0, column=2, padx=8, pady=10)
        ttk.Button(btn_frame, text="🛑 Stop", command=self.stop_sync).grid(row=0, column=3, padx=8, pady=10)

        # 3. Status Dashboard Section
        status_frame = ttk.LabelFrame(self, text=" Live Sync Status (Database) ")
        status_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.lbl_status = ttk.Label(status_frame, text="Status: IDLE", font=("Helvetica", 11, "bold"))
        self.lbl_status.pack(anchor="w", padx=15, pady=8)

        self.lbl_files = ttk.Label(status_frame, text="Scanned Files: 0", font=("Helvetica", 10))
        self.lbl_files.pack(anchor="w", padx=15, pady=3)

        self.lbl_folders = ttk.Label(status_frame, text="Scanned Folders: 0", font=("Helvetica", 10))
        self.lbl_folders.pack(anchor="w", padx=15, pady=3)

        self.lbl_job_id = ttk.Label(status_frame, text="Active Job ID: None", font=("Helvetica", 9), foreground="gray")
        self.lbl_job_id.pack(anchor="w", padx=15, pady=8)

    # UI Button Actions
    def start_sync(self):
        try:
            acc_id = int(self.ent_account_id.get().strip())
            drive_id = self.ent_drive_id.get().strip()
            self.sync_mgr.start_sync(account_id=acc_id, drive_id=drive_id)
        except ValueError:
            messagebox.showerror("Input Error", "Account ID သည် ကိန်းဂဏန်း (Number) ဖြစ်ရပါမည်။")

    def pause_sync(self):
        drive_id = self.ent_drive_id.get().strip()
        self.sync_mgr.pause_sync(drive_id)

    def resume_sync(self):
        drive_id = self.ent_drive_id.get().strip()
        self.sync_mgr.resume_sync(drive_id)

    def stop_sync(self):
        drive_id = self.ent_drive_id.get().strip()
        self.sync_mgr.stop_sync(drive_id)

    # Database ထဲမှ Status ကို 0.5 စက္ကန့်တစ်ကြိမ် Auto Polling ဆွဲယူစစ်ဆေးခြင်း
    def _start_status_polling(self):
        drive_id = self.ent_drive_id.get().strip()
        if drive_id:
            job = self.db.fetch_one(
                "SELECT id, status, scanned_files, scanned_folders FROM sync_jobs WHERE drive_id = ? ORDER BY id DESC LIMIT 1",
                (drive_id,)
            )
            if job:
                status_color = {
                    "running": "green",
                    "paused": "orange",
                    "cancelled": "red",
                    "completed": "blue",
                    "failed": "red"
                }.get(job["status"], "black")

                self.lbl_status.config(text=f"Status: {job['status'].upper()}", foreground=status_color)
                self.lbl_files.config(text=f"Scanned Files: {job['scanned_files']:,}")
                self.lbl_folders.config(text=f"Scanned Folders: {job['scanned_folders']:,}")
                self.lbl_job_id.config(text=f"Active Job ID: #{job['id']}")

        # 500ms (0.5s) အကြာတွင် Loop ပြန်ပတ်မည်
        self.after(500, self._start_status_polling)


if __name__ == "__main__":
    app = SyncTestApp()
    app.mainloop()