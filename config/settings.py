import tempfile
from pathlib import Path


# PC တိုင်းနှင့် ကိုက်ညီမည့် Dynamic Default Paths
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / "Nexora"
DEFAULT_TEMP_DIR = Path(tempfile.gettempdir()) / "NexoraTemp"


DEFAULT_APP_SETTINGS = {
    # Download Settings
    "default_download_path": (str(DEFAULT_DOWNLOAD_DIR), "download"),
    "temp_download_path": (str(DEFAULT_TEMP_DIR), "download"),
    "max_concurrent_downloads": ("3", "download"),
    "duplicate_file_action": ("auto_rename", "download"),
    "max_retries_per_item": ("5", "download"),
    "auto_resume_on_startup": ("true", "download"),

    # Network
    "speed_limit_kbps": ("0", "network"),
    "max_connections_per_file": ("4", "network"),

    # Google Defaults
    "default_export_doc": ("docx", "google"),
    "default_export_sheet": ("xlsx", "google"),
    "default_export_slide": ("pptx", "google"),
    "auto_sync_interval_minutes": ("30", "google"),

    # System & UI
    "prevent_sleep_during_download": ("true", "system"),
    "minimize_to_tray_on_close": ("true", "system"),
    "launch_on_startup": ("false", "system"),
    "theme": ("dark", "ui"),
    "notify_on_complete": ("true", "ui"),
    "play_sound_on_complete": ("true", "ui")
}


