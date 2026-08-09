from config.paths import DOWNLOAD_DIR

APP_NAME = "Nexora"
APP_VERSION = "1.0.0"

# Default Download Engine Settings
DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MB
DEFAULT_DOWNLOAD_PATH = DOWNLOAD_DIR  # User ရဲ့ Default Downloads/Nexora Folder
DEFAULT_CONNECTIONS = 4  # Max connections per server (Aria2 --max-connection-per-server)
DEFAULT_SPLIT = 4        # File split count (Aria2 --split)
SUPPORTED_CLOUDS = [ "Google Drive"]

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