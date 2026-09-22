# ============================================================
# Nexora - Application Configuration
# Version: 1.0.0
# ============================================================

from pathlib import Path

from config.app_paths import (
    APP_DATA_DIR,
    DATABASE_PATH,
    LOGS_DIR,
)

from config.app_constants import (
    GOOGLE_SCOPES,
    DEFAULT_CHUNK_SIZE,
)

from config.app_config_manager import ConfigManager


class AppConfig:
    """
    Nexora Application Configuration Facade.

    Application တစ်ခုလုံးအတွက်
    System Paths + Constants + User Settings
    များကို Single Interface ဖြင့် အသုံးပြုနိုင်ရန်
    Wrapper အဖြစ် လုပ်ဆောင်သည်။
    """

    def __init__(self):
        # ----------------------------------------------------
        # Application Paths
        # ----------------------------------------------------

        self.data_dir: Path = APP_DATA_DIR
        self.db_path: Path = DATABASE_PATH
        self.logs_dir: Path = LOGS_DIR

        # ----------------------------------------------------
        # Application Constants
        # ----------------------------------------------------

        self.scopes = GOOGLE_SCOPES
        self.chunk_size: int = DEFAULT_CHUNK_SIZE

        # ----------------------------------------------------
        # User Settings
        # ----------------------------------------------------

        self.settings = ConfigManager()

    # ========================================================
    # Download Settings
    # ========================================================

    @property
    def download_path(self) -> str:
        """Default download directory."""
        return self.settings.get("default_download_path")

    @property
    def temp_path(self) -> str:
        """Temporary download directory."""
        return self.settings.get("temp_download_path")

    @property
    def max_concurrent(self) -> int:
        """Maximum number of simultaneous downloads."""
        return int(
            self.settings.get(
                "max_concurrent_downloads",
                "3"
            )
        )

    @property
    def duplicate_file_action(self) -> str:
        """Action to take when a duplicate file exists."""
        return self.settings.get(
            "duplicate_file_action",
            "auto_rename"
        )

    @property
    def max_retries(self) -> int:
        """Maximum retry count for a download item."""
        return int(
            self.settings.get(
                "max_retries_per_item",
                "5"
            )
        )

    @property
    def auto_resume(self) -> bool:
        """Automatically resume unfinished downloads."""
        return self._to_bool(
            self.settings.get(
                "auto_resume_on_startup",
                "true"
            )
        )

    # ========================================================
    # Network Settings
    # ========================================================

    @property
    def speed_limit_kbps(self) -> int:
        """Global download speed limit in KB/s.

        0 = Unlimited
        """
        return int(
            self.settings.get(
                "speed_limit_kbps",
                "0"
            )
        )

    @property
    def max_connections_per_file(self) -> int:
        """Maximum connections per individual file."""
        return int(
            self.settings.get(
                "max_connections_per_file",
                "4"
            )
        )

    # ========================================================
    # Google Drive Settings
    # ========================================================

    @property
    def default_export_doc(self) -> str:
        return self.settings.get(
            "default_export_doc",
            "docx"
        )

    @property
    def default_export_sheet(self) -> str:
        return self.settings.get(
            "default_export_sheet",
            "xlsx"
        )

    @property
    def default_export_slide(self) -> str:
        return self.settings.get(
            "default_export_slide",
            "pptx"
        )

    @property
    def auto_sync_interval(self) -> int:
        """Google Drive auto-sync interval in minutes."""
        return int(
            self.settings.get(
                "auto_sync_interval_minutes",
                "30"
            )
        )

    # ========================================================
    # System Settings
    # ========================================================

    @property
    def prevent_sleep(self) -> bool:
        """Prevent system sleep while downloading."""
        return self._to_bool(
            self.settings.get(
                "prevent_sleep_during_download",
                "true"
            )
        )

    @property
    def minimize_to_tray(self) -> bool:
        """Minimize application to system tray on close."""
        return self._to_bool(
            self.settings.get(
                "minimize_to_tray_on_close",
                "true"
            )
        )

    @property
    def launch_on_startup(self) -> bool:
        """Launch Nexora automatically with Windows."""
        return self._to_bool(
            self.settings.get(
                "launch_on_startup",
                "false"
            )
        )

    # ========================================================
    # UI Settings
    # ========================================================

    @property
    def theme(self) -> str:
        return self.settings.get(
            "theme",
            "dark"
        )

    @property
    def notify_on_complete(self) -> bool:
        return self._to_bool(
            self.settings.get(
                "notify_on_complete",
                "true"
            )
        )

    @property
    def play_sound_on_complete(self) -> bool:
        return self._to_bool(
            self.settings.get(
                "play_sound_on_complete",
                "true"
            )
        )

    # ========================================================
    # Helpers
    # ========================================================

    @staticmethod
    def _to_bool(value: str | bool) -> bool:
        """
        String value ကို Python bool အဖြစ် ပြောင်းပေးသည်။

        Supported:
            "true", "1", "yes", "on"  -> True
            "false", "0", "no", "off" -> False
        """

        if isinstance(value, bool):
            return value

        return str(value).strip().lower() in {
            "true",
            "1",
            "yes",
            "on",
        }
