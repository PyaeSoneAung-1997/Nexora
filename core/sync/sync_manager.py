from core.sync.sync_worker import SyncWorker
import os
from core.download.download_manager import DownloadManager
from core.database.db_manager import DatabaseManager

class SyncManager:
    """အကောင့်အလိုက်၊ Drive အလိုက် Worker Thread များကို Centralize ထိန်းချုပ်မည့် Manager"""

    def __init__(self):
        self.active_workers: dict[str, SyncWorker] = {}  # Key = drive_id, Value = SyncWorker

    def start_sync(self, account_id: int, drive_id: str = "root", drive_type: str = "my_drive", drive_name: str = "My Drive", job_id: int = None, download_path: str = None) -> SyncWorker:
        """Sync Job အသစ်စတင်မည် သို့မဟုတ် ရပ်ထားသော Job ကို Resume အဖြစ် ပြန်စမည်"""
        if drive_id in self.active_workers and self.active_workers[drive_id].is_alive():
            print(f"⚠️ Worker for Drive {drive_id} is already running.")
            return self.active_workers[drive_id]

        worker = SyncWorker(
            account_id=account_id,
            drive_id=drive_id,
            drive_type=drive_type,
            drive_name=drive_name,
            job_id=job_id
        )
        self.active_workers[drive_id] = worker
        worker.start()
        return worker

    def pause_sync(self, drive_id: str):
        if drive_id in self.active_workers:
            self.active_workers[drive_id].pause()

    def resume_sync(self, drive_id: str):
        if drive_id in self.active_workers:
            self.active_workers[drive_id].resume()

    def stop_sync(self, drive_id: str):
        if drive_id in self.active_workers:
            self.active_workers[drive_id].stop()
            del self.active_workers[drive_id]

    def create_download_job_from_scanned_files(self, account_id: int, download_path: str):
            """Scanned ဖိုင်များကို Download Queue ထဲသို့ ပြောင်းလဲထည့်သွင်း၍ Download စတင်မည်"""
            self.download_mgr = DownloadManager()
            self.db = DatabaseManager()
            # 1. Download Queue အသစ်ဆောက်မည်
            queue_id = self.download_mgr.create_queue(account_id=account_id, title="My Drive Sync Queue")
            
            # 2. DB ထဲရှိ Scan ဖတ်ထားသော ဖိုင်များကို ဆွဲထုတ်မည်
            files = self.db.fetch_all(
                "SELECT id, name, mime_type FROM drive_files WHERE account_id = ? AND mime_type != 'application/vnd.google-apps.folder'", 
                (account_id,)
            )
            
            # 3. File တစ်ခုချင်းစီကို download_items ထဲ ထည့်မည်
            for file in files:
                dest_file_path = os.path.join(download_path, file["name"])
                temp_file_path = dest_file_path + ".tmp"
                
                # Google Docs/Sheets ဖြစ်ပါက Export Mime Type သတ်မှတ်မည်
                export_mime = None
                if "vnd.google-apps.document" in file["mime_type"]:
                    export_mime = "application/pdf"
                elif "vnd.google-apps.spreadsheet" in file["mime_type"]:
                    export_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
                self.download_mgr.add_item_to_queue(
                    queue_id=queue_id,
                    drive_file_id=file["id"],
                    destination_path=dest_file_path,
                    temp_path=temp_file_path,
                    export_mime_type=export_mime
                )
    
            # 4. aria2c Downloader Engine ဖြင့် ဒေါင်းလုဒ်စတင်မည်
            self.download_mgr.start_queue(queue_id)
            return queue_id
