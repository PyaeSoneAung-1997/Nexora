from config.paths import DOWNLOAD_DIR

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