# ============================================================
# Nexora - Application Constants
# Version: 1.0.0
# ============================================================

# ------------------------------------------------------------
# Application Information
# ------------------------------------------------------------

APP_NAME = "Nexora"
APP_VERSION = "1.0.0"


# ------------------------------------------------------------
# Google Drive Authentication
# ------------------------------------------------------------

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


# ------------------------------------------------------------
# Download Engine Defaults
# ------------------------------------------------------------

DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MB
DEFAULT_CONNECTIONS = 4            # Max connections per server
DEFAULT_SPLIT = 4                  # File split count


# ------------------------------------------------------------
# Supported Cloud Providers
# ------------------------------------------------------------

SUPPORTED_CLOUDS = [
    "Google Drive",
]


# ------------------------------------------------------------
# Download Status
# ------------------------------------------------------------

DOWNLOAD_STATUS = (
    "queued",
    "downloading",
    "paused",
    "completed",
    "failed",
    "cancelled",
)


# ------------------------------------------------------------
# Sync Status
# ------------------------------------------------------------

SYNC_STATUS = (
    "queued",
    "scanning",
    "paused",
    "completed",
    "failed",
)


# ------------------------------------------------------------
# Google Workspace Export MIME Types
# ------------------------------------------------------------

WORKSPACE_EXPORT_MIME_MAP = {
    "application/vnd.google-apps.document":
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

    "application/vnd.google-apps.spreadsheet":
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    "application/vnd.google-apps.presentation":
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


# ------------------------------------------------------------
# Google Workspace Export Extensions
# ------------------------------------------------------------

WORKSPACE_EXPORT_EXT_MAP = {
    "application/vnd.google-apps.document": "docx",
    "application/vnd.google-apps.spreadsheet": "xlsx",
    "application/vnd.google-apps.presentation": "pptx",
}
