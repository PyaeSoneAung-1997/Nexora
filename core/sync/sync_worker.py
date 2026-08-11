import threading
from core.database.db_manager import DatabaseManager
from core.cloud.auth_manager import GoogleAuthManager
from core.cloud.drive_scanner import DriveScanner


class SyncWorker(threading.Thread):
    """Background Thread ဖြင့် Drive Sync/Scan ပြုလုပ်ခြင်းနှင့် Pause/Resume/Stop တို့ကို ထိန်းချုပ်မည့် Worker Class"""

    def __init__(
        self,
        account_id: int,
        drive_id: str = "root",
        drive_type: str = "my_drive",  # 'my_drive' သို့မဟုတ် 'shared_drive'
        drive_name: str = "My Drive",
        job_id: int = None,
        auth_manager: GoogleAuthManager = None,
        db_manager: DatabaseManager = None
    ):
        super().__init__()
        self.account_id = account_id
        self.drive_id = drive_id
        self.drive_type = drive_type
        self.drive_name = drive_name
        self.job_id = job_id

        self.db = db_manager or DatabaseManager()
        self.auth_mgr = auth_manager or GoogleAuthManager()
        self.scanner = DriveScanner(auth_manager=self.auth_mgr, db_manager=self.db)

        # Thread Control Events
        self._pause_event = threading.Event()
        self._pause_event.set()  # True = Active/Running, False = Paused
        self._stop_event = threading.Event()   # True = Stop Requested

    def run(self):
        """Background Thread အဖြစ် Scan Process ကို စတင်ပတ်ပေးမည့် Main Logic"""
        try:
            # 1. Job ID မရှိသေးပါက sync_jobs ထဲတွင် အသစ်စတင်တည်ဆောက်မည်
            if not self.job_id:
                job_query = """
                    INSERT INTO sync_jobs (account_id, drive_id, job_type, status, started_at, updated_at)
                    VALUES (?, ?, 'scan', 'running', datetime('now', 'localtime'), datetime('now', 'localtime'))
                """
                self.job_id = self.db.execute_query(job_query, (self.account_id, self.drive_id))
            else:
                self.db.execute_query(
                    "UPDATE sync_jobs SET status = 'running', updated_at = datetime('now', 'localtime') WHERE id = ?",
                    (self.job_id,)
                )

            # 2. Drive Type အပေါ်မူတည်၍ Scanner ခေါ်ယူခြင်း
            if self.drive_type == "shared_drive":
                result = self.scanner.scan_single_shared_drive(
                    account_id=self.account_id,
                    shared_drive_id=self.drive_id,
                    shared_drive_name=self.drive_name,
                    job_id=self.job_id,
                    pause_event=self._pause_event,
                    stop_event=self._stop_event
                )
            else:
                result = self.scanner.scan_my_drive(
                    account_id=self.account_id,
                    job_id=self.job_id,
                    pause_event=self._pause_event,
                    stop_event=self._stop_event
                )

            print(f"✅ Sync Job #{self.job_id} Finished Successfully: {result}")

        except Exception as e:
            print(f"❌ Sync Job #{self.job_id} Failed: {e}")

    def pause(self):
        """Sync လုပ်ငန်းစဉ်ကို ခဏရပ်ဆိုင်းမည်"""
        self._pause_event.clear()  # Scanner ထဲရှိ pause_event.wait() တွင် တန့်ရပ်သွားမည်
        if self.job_id:
            self.db.execute_query(
                "UPDATE sync_jobs SET status = 'paused', updated_at = datetime('now', 'localtime') WHERE id = ?",
                (self.job_id,)
            )
            self.db.execute_query(
                "UPDATE drives SET status = 'paused' WHERE drive_id = ?",
                (self.drive_id,)
            )
        print(f"⏸️ Job #{self.job_id} Paused")

    def resume(self):
        """Pause ရပ်ထားသော Sync ကို ပြန်လည်စတင်မည်"""
        self._pause_event.set()  # wait() ကို ကျော်ဖြတ်ပြီး ဆက်သွားစေမည်
        if self.job_id:
            self.db.execute_query(
                "UPDATE sync_jobs SET status = 'running', updated_at = datetime('now', 'localtime') WHERE id = ?",
                (self.job_id,)
            )
            self.db.execute_query(
                "UPDATE drives SET status = 'scanning' WHERE drive_id = ?",
                (self.drive_id,)
            )
        print(f"▶️ Job #{self.job_id} Resumed")

    def stop(self):
        """Sync ကို လုံးဝ အပြီးတိုင် ရပ်တန့်မည်"""
        self._stop_event.set()
        self._pause_event.set()  # Pause ဖြစ်နေပါက ရပ်မနေဘဲ Loop ထဲမှ ချက်ချင်းထွက်နိုင်ရန် Unblock ပြုလုပ်ခြင်း
        if self.job_id:
            self.db.execute_query(
                "UPDATE sync_jobs SET status = 'cancelled', updated_at = datetime('now', 'localtime') WHERE id = ?",
                (self.job_id,)
            )
            self.db.execute_query(
                "UPDATE drives SET status = 'idle' WHERE drive_id = ?",
                (self.drive_id,)
            )
        print(f"🛑 Job #{self.job_id} Stopped")