from config.app_paths import DOWNLOAD_DIR, DEFAULT_DOWNLOAD_DIR, DEFAULT_TEMP_DIR

# App Information
APP_NAME = "Nexora"
APP_VERSION = "1.0.0"

# Google Auth Scopes
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Default Download Engine Settings
DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk
DEFAULT_DOWNLOAD_PATH = DOWNLOAD_DIR  # User ရဲ့ Default Downloads/Nexora Folder
DEFAULT_CONNECTIONS = 4  # Max connections per server
DEFAULT_SPLIT = 4  # File split count
SUPPORTED_CLOUDS = ["Google Drive"]

# Status Definitions
DOWNLOAD_STATUS = (
    "queued",
    "downloading",
    "paused",
    "completed",
    "failed",
    "cancelled",
)

SYNC_STATUS = (
    "queued",
    "scanning",
    "paused",
    "completed",
    "failed",
)

# Google Workspace File Export Mappings
WORKSPACE_EXPORT_MIME_MAP = {
    "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
    "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",      # xlsx
    "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation"  # pptx
}

WORKSPACE_EXPORT_EXT_MAP = {
    "application/vnd.google-apps.document": "docx",
    "application/vnd.google-apps.spreadsheet": "xlsx",
    "application/vnd.google-apps.presentation": "pptx"
}

DEFAULT_APP_SETTINGS = {
    "default_download_path": (str(DEFAULT_DOWNLOAD_DIR), "download"),
    "temp_download_path": (str(DEFAULT_TEMP_DIR), "download"),
    "max_concurrent_downloads": ("3", "download"),
    "duplicate_file_action": ("auto_rename", "download"),
    "max_retries_per_item": ("5", "download"),
    "auto_resume_on_startup": ("true", "download"),
    "speed_limit_kbps": ("0", "network"),
    "max_connections_per_file": ("4", "network"),
    "default_export_doc": ("docx", "google"),
    "default_export_sheet": ("xlsx", "google"),
    "default_export_slide": ("pptx", "google"),
    "auto_sync_interval_minutes": ("30", "google"),
    "prevent_sleep_during_download": ("true", "system"),
    "minimize_to_tray_on_close": ("true", "system"),
    "launch_on_startup": ("false", "system"),
    "theme": ("dark", "ui"),
    "notify_on_complete": ("true", "ui"),
    "play_sound_on_complete": ("true", "ui")
}