import sqlite3
from pathlib import Path
import os

APP_NAME = "Nexora"
SYSTEM_APPDATA = os.getenv("APPDATA") or os.path.expanduser("~")
APP_DATA_DIR = Path(SYSTEM_APPDATA) / APP_NAME 

# Folder မရှိသေးပါက အလိုအလျောက် ဆောက်ပေးမည်
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = APP_DATA_DIR / "nexora.db"

def get_connection() -> sqlite3.Connection:
    """WAL Mode နှင့် Foreign Key constraint များ ပါဝင်သော SQLite Connection ထုတ်ပေးမည်"""
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn  # <-- ဒီနေရာမှာ return ပြန်ပေးရန် လိုအပ်သည်

def execute_query(query: str, params: tuple = ()) -> int:
    """INSERT, UPDATE, DELETE query တစ်ခုတည်း လုပ်ဆောင်ရန်"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

job_id = 25
account_id = 1
drive_id = "root"

if not job_id:
    job_query = """
        INSERT INTO sync_jobs (account_id, drive_id, job_type, status, started_at, updated_at)
        VALUES (?, ?, 'scan', 'running', datetime('now', 'localtime'), datetime('now', 'localtime'))
    """
    job_id = execute_query(job_query, (account_id, drive_id))
    print(f"Created new job ID: {job_id}")
else:
    update_query = """
        UPDATE sync_jobs 
        SET status = 'running', updated_at = datetime('now', 'localtime') 
        WHERE id = ?
    """
    execute_query(update_query, (job_id,)) # job_id ကို ပြန်မသိမ်းဘဲ update သာ လုပ်မည်
    print(f"Updated job ID: {job_id}")


       