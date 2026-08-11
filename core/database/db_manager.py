import sqlite3
from pathlib import Path
from config.app_paths import DATABASE_PATH
from config.app_constants import DEFAULT_APP_SETTINGS
from core.database.schema import CREATE_SCHEMA_SQL


class DatabaseManager:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.DATABASE_PATH = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        """WAL Mode နှင့် Foreign Key constraint များ ပါဝင်သော SQLite Connection ထုတ်ပေးမည်"""
        conn = sqlite3.connect(self.DATABASE_PATH, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_db(self):
        """Database ဇယားများ ဆောက်ပြီး Dynamic Default Settings များကို ထည့်ပေးမည်"""
        with self.get_connection() as conn:
            # 1. Execute SQL DDL Schema
            conn.executescript(CREATE_SCHEMA_SQL)
            
            # 2. Seed Dynamic Defaults into app_settings table
            cursor = conn.cursor()
            for key, (value, category) in DEFAULT_APP_SETTINGS.items():
                cursor.execute("""
                    INSERT OR IGNORE INTO app_settings (key, value, category)
                    VALUES (?, ?, ?)
                """, (key, value, category))
                
            conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> int:
        """INSERT, UPDATE, DELETE query တစ်ခုတည်း လုပ်ဆောင်ရန်"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def execute_many(self, query: str, params_list: list[tuple]) -> None:
        """INSERT, UPDATE batch processing များ အများအပြား တစ်ပြိုင်နက် လုပ်ဆောင်ရန်"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict]:
        """SELECT Query များဖြင့် List of Dicts ထုတ်ယူရန်"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def fetch_one(self, query: str, params: tuple = ()) -> dict | None:
        """SELECT Query မှ Record တစ်ခုတည်း ထုတ်ယူရန်"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None