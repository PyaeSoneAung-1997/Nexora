import os
import re
import shutil
import time
import subprocess
import threading
from core.cloud.auth_manager import GoogleAuthManager
from core.database.db_manager import DatabaseManager
from config.app_paths import ARIA2_PATH


class DriveDownloader:
    """Download Item တစ်ခုချင်းစီကို aria2c သုံး၍ အရှိန်မြှင့် ဒေါင်းလုဒ်ဆွဲပေးမည့် Core Engine"""

    def __init__(self, auth_manager: GoogleAuthManager = None, db_manager: DatabaseManager = None):
        self.auth_mgr = auth_manager or GoogleAuthManager()
        self.db = db_manager or DatabaseManager()

    def get_access_token(self, account_id: int) -> str:
        """Account ID မှ Active Credentials ရယူပြီး Access Token ထုတ်ပေးမည်"""
        creds = self.auth_mgr.get_credentials(account_id)
        if not creds:
            raise ValueError(f"Account ID {account_id} အတွက် Active Credentials မရှိပါ။")
        
        # Token သက်တမ်းကုန်နေပါက Refresh လုပ်မည်
        if creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
            
        return creds.token

    def download_item(
        self, item_id: int, 
        pause_event: threading.Event = None, 
        stop_event: threading.Event = None
    ) -> dict:
        """Download Item တစ်ခုကို aria2c ဖြင့် စတင်/ဆက်လက် ဒေါင်းလုဒ်ဆွဲမည်"""
        
        # 1. DB မှ Item, Drive File နှင့် Queue အချက်အလက်များကို ဆွဲထုတ်မည်
        query = """
            SELECT 
                di.*, 
                df.file_id AS gdrive_file_id, 
                df.name AS file_name, 
                df.mime_type, 
                df.md5_checksum,
                dq.account_id, 
                dq.title AS queue_title
            FROM download_items di
            JOIN drive_files df ON di.drive_file_id = df.id
            JOIN download_queues dq ON di.queue_id = dq.id
            WHERE di.id = ?
        """
        item = self.db.fetch_one(query, (item_id,))
        if not item:
            raise ValueError(f"Download Item ID {item_id} ကို ရှာမတွေ့ပါ။")

        account_id = item["account_id"]
        gdrive_file_id = item["gdrive_file_id"]
        file_name = item["file_name"]
        mime_type = item["mime_type"]
        temp_path = item["temp_path"]
        destination_path = item["destination_path"]
        export_mime_type = item["export_mime_type"]

        # OAuth Access Token ရယူခြင်း
        token = self.get_access_token(account_id)

        temp_dir = os.path.dirname(temp_path)
        temp_file_name = os.path.basename(temp_path)
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Google Docs/Sheets သို့မဟုတ် ပုံမှန် Drive File အလိုက် Download URL သတ်မှတ်ခြင်း
        if export_mime_type:
            download_url = f"https://www.googleapis.com/drive/v3/files/{gdrive_file_id}/export?mimeType={export_mime_type}"
        else:
            download_url = f"https://www.googleapis.com/drive/v3/files/{gdrive_file_id}?alt=media"

        # Item & Queue Status ကို 'downloading' ပြောင်းမည်
        start_time = time.time()
        self.db.execute_query("""
            UPDATE download_items 
            SET status = 'downloading', started_at = datetime('now', 'localtime') 
            WHERE id = ?
        """, (item_id,))
        self.db.execute_query("""
            UPDATE download_queues 
            SET status = 'running' 
            WHERE id = ?
        """, (item["queue_id"],))

        # aria2c Command ပြင်ဆင်ခြင်း
        aria2_cmd = [
             ARIA2_PATH if os.path.exists(ARIA2_PATH) else "aria2c",
            "-x", "16",                            # Server တစ်ခုလျှင် Connection 16 ခု ခွဲမည်
            "-s", "16",                            # Max connections
            "-k", "1M",                            # Chunk size
            "-c",                                  # Continue / Resume support
            "-d", temp_dir,                        # Directory
            "-o", temp_file_name,                  # Save as temp filename
            f"--header=Authorization: Bearer {token}", # Google Auth Token Header
            "--file-allocation=none",
            "--summary-interval=1",               # Speed status update တိုင်းတာရန်
            download_url
        ]

        try:
            # aria2c ကို Subprocess ဖြင့် စတင်မောင်းနှင်ခြင်း
            process = subprocess.Popen(
                aria2_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True
            )

            # Process Output ကို တစ်ကြောင်းချင်းစီဖတ်ပြီး DB/Events များ စစ်ဆေးမည်
            while True:
                # Stop / Cancel Event စစ်ဆေးခြင်း
                if stop_event and stop_event.is_set():
                    process.terminate()
                    self.db.execute_query("UPDATE download_items SET status = 'cancelled' WHERE id = ?", (item_id,))
                    return {"status": "cancelled", "item_id": item_id}

                # Pause Event စစ်ဆေးခြင်း
                if pause_event and not pause_event.is_set():
                    process.terminate()
                    self.db.execute_query("UPDATE download_items SET status = 'paused' WHERE id = ?", (item_id,))
                    pause_event.wait() # Resume လုပ်သည်အထိ စောင့်မည်
                    # Pause ဖြုတ်ပါက Function ကို ပြန်လည် စတင်ရန် (Recursive call)
                    return self.download_item(item_id, pause_event, stop_event)

                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break

                # aria2c output ထဲမှ Speed/Progress ရယူရန် (Regex)
                if output:
                    # ဥပမာ- [#b3f200 12MiB/20MiB(60%) CN:16 DL:2.5MiB]
                    match = re.search(r'\((\d+)%\).*?DL:([\d\.]+\w+)', output)
                    if match and os.path.exists(temp_path):
                        current_bytes = os.path.getsize(temp_path)
                        self.db.execute_query("""
                            UPDATE download_items 
                            SET downloaded_bytes = ? 
                            WHERE id = ?
                        """, (current_bytes, item_id))

            if process.returncode != 0:
                raise RuntimeError(f"aria2c process failed with return code {process.returncode}")

            # 2. ဒေါင်းလုဒ်အောင်မြင်ပါက Temp Path မှ Destination Path သို့ ရွှေ့မည်
            if os.path.exists(destination_path):
                os.remove(destination_path)
            shutil.move(temp_path, destination_path)

            end_time = time.time()
            duration_seconds = max(1, int(end_time - start_time))
            file_size = os.path.getsize(destination_path)
            avg_speed = int(file_size / duration_seconds)

            # Item Status Update
            self.db.execute_query("""
                UPDATE download_items 
                SET status = 'completed', downloaded_bytes = total_size, completed_at = datetime('now', 'localtime') 
                WHERE id = ?
            """, (item_id,))

            # Queue Status Update
            self.db.execute_query("""
                UPDATE download_queues 
                SET completed_files = completed_files + 1,
                    downloaded_bytes = downloaded_bytes + ?
                WHERE id = ?
            """, (file_size, item["queue_id"]))

            # 3. Download History သို့ မှတ်တမ်းထည့်သွင်းခြင်း
            self.db.execute_query("""
                INSERT INTO download_history (
                    account_id, file_id, file_name, mime_type, file_size, avg_speed, 
                    duration_seconds, destination_path, md5_checksum, queue_title, 
                    status, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', datetime('now', 'localtime'))
            """, (
                account_id, gdrive_file_id, file_name, mime_type, file_size, avg_speed,
                duration_seconds, destination_path, item["md5_checksum"], item["queue_title"]
            ))

            return {"status": "completed", "item_id": item_id}

        except Exception as e:
            self.db.execute_query("""
                UPDATE download_items 
                SET status = 'failed', error_message = ? 
                WHERE id = ?
            """, (str(e), item_id))

            # History တွင် Error အဖြစ် မှတ်တမ်းတင်မည်
            self.db.execute_query("""
                INSERT INTO download_history (
                    account_id, file_id, file_name, mime_type, destination_path, 
                    queue_title, status, error_message, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'failed', ?, datetime('now', 'localtime'))
            """, (account_id, gdrive_file_id, file_name, mime_type, destination_path, item["queue_title"], str(e)))

            raise e