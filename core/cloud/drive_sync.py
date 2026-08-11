import threading
import time
from core.database.db_manager import DatabaseManager


class SyncWorker(threading.Thread):
    def __init__(self, job_id: int, account_id: int, drive_id: str, db_manager: DatabaseManager = None):
        super().__init__()
        self.job_id = job_id
        self.account_id = account_id
        self.drive_id = drive_id
        self.db = db_manager or DatabaseManager()

        # Thread Control Events
        self._pause_event = threading.Event()
        self._pause_event.set()  # True = Running, False = Paused
        self._stop_event = threading.Event()   # True = Stop requested

    def run(self):
        """Sync Process ကို Thread နောက်ကွယ်တွင် စတင်ပတ်ပေးသည့် Main Loop"""
        # 1. DB မှ နောက်ဆုံး သိမ်းထားခဲ့သော next_page_token ကို ပြန်ယူသည်
        job = self.db.fetch_one("SELECT next_page_token FROM sync_jobs WHERE id = ?", (self.job_id,))
        page_token = job["next_page_token"] if job else None

        self._update_job_status("scanning")

        try:
            while not self._stop_event.is_set():
                # Pause လုပ်ထားပါက တန့်ရပ်နေမည် (Resume နှိပ်မှ ဆက်သွားမည်)
                self._pause_event.wait()

                # Pause ဖြုတ်ပြီးချိန်တွင် Stop နှိပ်ခံရခြင်း ရှိမရှိ အမြဲပြန်စစ်သည်
                if self._stop_event.is_set():
                    break

                # 2. Google Drive API သို့ Fetch ခေါ်ခြင်း (Mock / Real API Call)
                # response = drive_service.files().list(pageToken=page_token, ...).execute()
                # files = response.get('files', [])
                # page_token = response.get('nextPageToken')

                # Dummy simulation for testing:
                time.sleep(1)  # API Call ပြုလုပ်နေသကဲ့သို့ ခေတ္တစောင့်ခြင်း
                
                # 3. ရလာသော ဖိုင်များကို Resolver မှတစ်ဆင့် DB ထဲ တန်းထည့်ခြင်း
                # save_files_to_db(files)

                # 4. Progress နှင့် Next Page Token ကို DB တွင် Update လုပ်ခြင်း
                self._update_job_status("scanning", next_token=page_token)

                # Next Page Token မရှိတော့ပါက Scan ပတ်ခြင်း ပြီးဆုံးပြီ
                if not page_token:
                    self._update_job_status("completed")
                    break

        except Exception as e:
            self._update_job_status("failed", error_msg=str(e))
            return

        # Stop ခေါ်ယူခံရပါက Status ကို 'cancelled' ဟု ပြောင်းမည်
        if self._stop_event.is_set():
            self._update_job_status("cancelled")

    def pause(self):
        """Sync ခဏရပ်ဆိုင်းမည်"""
        self._pause_event.clear()  # wait() တွင် ခေတ္တ ရပ်တန့်သွားစေမည်
        self._update_job_status("paused")

    def resume(self):
        """Pause လုပ်ထားသော Sync ကို ပြန်လည်စတင်မည်"""
        self._pause_event.set()    # wait() ကို ကျော်ဖြတ်ပြီး ပတ်လက်စ Loop မှ ဆက်သွားမည်
        self._update_job_status("scanning")

    def stop(self):
        """Sync ကို လုံးဝ ရပ်တန့်ပစ်မည်"""
        self._stop_event.set()
        self._pause_event.set()    # Pause ဖြစ်နေပါက အပြင်ထွက်နိုင်ရန် Pause ကို ဖြေပေးရမည်
        self._update_job_status("cancelled")

    def _update_job_status(self, status: str, next_token: str = None, error_msg: str = None):
        """DB ထဲရှိ sync_jobs Table ကို Status Update ပြုလုပ်ပေးသည့် Helper"""
        sql = """
        UPDATE sync_jobs 
        SET status = ?, 
            next_page_token = COALESCE(?, next_page_token),
            error_message = ?,
            updated_at = datetime('now', 'localtime')
        WHERE id = ?
        """
        self.db.execute_query(sql, (status, next_token, error_msg, self.job_id))