from config.paths import APP_DATA_DIR, DATABASE_PATH, LOGS_DIR
from config.constants import GOOGLE_SCOPES, DEFAULT_CHUNK_SIZE
from core.database.db_manager import DatabaseManager


class AppConfig:
    """System Configurations များကို Single Interface ဖွငျ့ ခေါျယူအသုံးပွုနိုငျသညျ့ Wrapper"""

    def __init__(self):
        self.data_dir = APP_DATA_DIR
        self.db_path = DATABASE_PATH
        self.logs_dir = LOGS_DIR
        self.scopes = GOOGLE_SCOPES
        self.chunk_size = DEFAULT_CHUNK_SIZE
        self.settings = ConfigManager()

    @property
    def download_path(self) -> str:
        return self.settings.get("default_download_path")

    @property
    def temp_path(self) -> str:
        return self.settings.get("temp_download_path")

    @property
    def max_concurrent(self) -> int:
        return int(self.settings.get("max_concurrent_downloads", "3"))

    @property
    def theme(self) -> str:
        return self.settings.get("theme", "dark")
    
class ConfigManager:
    """Database app_settings ဇယားမှ Dynamic Settings များကို ဖတ်/ရေး ရန် Class"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()

    def get(self, key: str, default: str = None) -> str:
        row = self.db.fetch_one("SELECT value FROM app_settings WHERE key = ?", (key,))
        return row["value"] if row else default

    def set(self, key: str, value: str) -> None:
        self.db.execute_query(
            "UPDATE app_settings SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?",
            (str(value), key)
        )

    def get_category(self, category: str) -> dict:
        rows = self.db.fetch_all("SELECT key, value FROM app_settings WHERE category = ?", (category,))
        return {row["key"]: row["value"] for row in rows}