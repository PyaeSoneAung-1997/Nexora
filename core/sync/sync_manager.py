from core.sync.sync_worker import SyncWorker

class SyncManager:
    """အကောင့်အလိုက်၊ Drive အလိုက် Worker Thread များကို Centralize ထိန်းချုပ်မည့် Manager"""

    def __init__(self):
        self.active_workers: dict[str, SyncWorker] = {}  # Key = drive_id, Value = SyncWorker

    def start_sync(self, account_id: int, drive_id: str = "root", drive_type: str = "my_drive", drive_name: str = "My Drive", job_id: int = None) -> SyncWorker:
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