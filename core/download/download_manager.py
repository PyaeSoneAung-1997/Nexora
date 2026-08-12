import threading
from core.download.drive_downloader import DriveDownloader
from core.database.db_manager import DatabaseManager


class DownloadManager:
    """Download Queues နှင့် Items များကို Thread ဖြင့် စီမံခန့်ခွဲပေးမည့် Controller"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
        self.downloader = DriveDownloader(db_manager=self.db)

        # Thread Control Events Dicts {item_id: Event}
        self.active_threads = {}
        self.pause_events = {}
        self.stop_events = {}

    # --- Queue & Item Creation ---
    def create_queue(self, account_id: int, title: str) -> int:
        """ Queue အသစ် တည်ဆောက်မည် """
        query = "INSERT INTO download_queues (account_id, title, status) VALUES (?, ?, 'queued')"
        return self.db.execute_query(query, (account_id, title))

    def add_item_to_queue(
        self, queue_id: int, drive_file_id: int, destination_path: str, temp_path: str, export_mime_type: str = None
    ) -> int:
        """ Queue ထဲသို့ Download Item အသစ် ထည့်သွင်းမည် """
        query = """
            INSERT INTO download_items (queue_id, drive_file_id, destination_path, temp_path, export_mime_type, status)
            VALUES (?, ?, ?, ?, ?, 'queued')
        """
        item_id = self.db.execute_query(query, (queue_id, drive_file_id, destination_path, temp_path, export_mime_type))
        
        # Queue ၏ total_files အရေအတွက် တိုးပေးမည်
        self.db.execute_query("UPDATE download_queues SET total_files = total_files + 1 WHERE id = ?", (queue_id,))
        return item_id

    # --- Queue Level Execution ---
    def start_queue(self, queue_id: int):
        """ Queue တစ်ခုလုံးတွင် ရှိသော 'queued' / 'paused' ဖြစ်နေသည့် Item များကို အစဉ်လိုက် ဒေါင်းလုဒ်ဆွဲမည် """
        thread = threading.Thread(target=self._run_queue, args=(queue_id,), daemon=True)
        thread.start()

    def _run_queue(self, queue_id: int):
        items = self.db.fetch_all("""
            SELECT id FROM download_items 
            WHERE queue_id = ? AND status IN ('queued', 'paused', 'failed') 
            ORDER BY order_index ASC, id ASC
        """, (queue_id,))

        for item in items:
            item_id = item["id"]
            self.start_item(item_id)
            # Item ဒေါင်းလုဒ်ဆွဲပြီးသည်အထိ တလှည့်စီ စောင့်မည်
            if item_id in self.active_threads:
                self.active_threads[item_id].join()

        # Queue ထဲရှိ Items အားလုံး ပြီးသွားပါက Queue Status ကို 'completed' ပြောင်းမည်
        self.db.execute_query("""
            UPDATE download_queues SET status = 'completed', completed_at = datetime('now', 'localtime') WHERE id = ?
        """, (queue_id,))

    def pause_queue(self, queue_id: int):
        """ Queue တစ်ခုလုံးရှိ အလုပ်လုပ်နေသော Item များကို ခေတ္တရပ်မည် """
        items = self.db.fetch_all("SELECT id FROM download_items WHERE queue_id = ? AND status = 'downloading'", (queue_id,))
        for item in items:
            self.pause_item(item["id"])
        self.db.execute_query("UPDATE download_queues SET status = 'paused' WHERE id = ?", (queue_id,))

    def stop_queue(self, queue_id: int):
        """ Queue တစ်ခုလုံးကို လုံးဝ ဖျက်သိမ်းမည် """
        items = self.db.fetch_all("SELECT id FROM download_items WHERE queue_id = ? AND status IN ('downloading', 'paused')", (queue_id,))
        for item in items:
            self.stop_item(item["id"])
        self.db.execute_query("UPDATE download_queues SET status = 'cancelled' WHERE id = ?", (queue_id,))

    # --- Individual Item Controls ---
    def start_item(self, item_id: int):
        """ Item တစ်ခုတည်းကို ဒေါင်းလုဒ် စတင်မည် """
        if item_id in self.active_threads and self.active_threads[item_id].is_alive():
            return

        pause_event = threading.Event()
        pause_event.set()
        stop_event = threading.Event()

        self.pause_events[item_id] = pause_event
        self.stop_events[item_id] = stop_event

        thread = threading.Thread(
            target=self.downloader.download_item,
            args=(item_id, pause_event, stop_event),
            daemon=True
        )
        self.active_threads[item_id] = thread
        thread.start()

    def pause_item(self, item_id: int):
        """ Item တစ်ခုတည်းကို ခေတ္တရပ်မည် """
        if item_id in self.pause_events:
            self.pause_events[item_id].clear()

    def resume_item(self, item_id: int):
        """ Item တစ်ခုတည်းကို ပြန်လည် စတင်မည် """
        if item_id in self.pause_events and self.active_threads.get(item_id, None) and self.active_threads[item_id].is_alive():
            self.pause_events[item_id].set()
        else:
            self.start_item(item_id)

    def stop_item(self, item_id: int):
        """ Item တစ်ခုတည်းကို လုံးဝ ဖျက်သိမ်းမည် """
        if item_id in self.stop_events:
            self.stop_events[item_id].set()
            if item_id in self.pause_events:
                self.pause_events[item_id].set()

    # --- History & UI Data ---
    def get_history_list(self) -> list[dict]:
        """ Download History စာရင်း ထုတ်ယူမည် """
        return self.db.fetch_all("SELECT * FROM download_history ORDER BY completed_at DESC")