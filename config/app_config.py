from config.app_paths import APP_DATA_DIR, DATABASE_PATH, LOGS_DIR
from config.app_constants import GOOGLE_SCOPES, DEFAULT_CHUNK_SIZE
from config.app_config_manager import ConfigManager



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
    
 