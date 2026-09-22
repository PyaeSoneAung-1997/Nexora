import os
import sys
import tempfile
from pathlib import Path

APP_NAME = "Nexora"

# 1. Base Directory (Bundled Read-Only Files)

if getattr(sys, "frozen", False):
    #PyInstaller EXE
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Running from source
    BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Bundled Application Resources
RESOURCES_DIR = BASE_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
STYLES_DIR = RESOURCES_DIR / "styles"

# 3. Aria2
ARIA2_DIR = BASE_DIR / "aria2"
ARIA2_PATH = ARIA2_DIR / "aria2c.exe"

# 4. Application Data Directory ( Writable Runtime Data )
SYSTEM_APPDATA = os.getenv("APPDATA") or os.path.expanduser("~")

APP_DATA_DIR = Path(SYSTEM_APPDATA) / APP_NAME

# 5. Google OAuth
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"


# 6. Runtime Data Paths
DATABASE_PATH = APP_DATA_DIR / "nexora.db"

DOWNLOAD_DIR  = APP_DATA_DIR / "downloads" 
TEMP_DIR = APP_DATA_DIR / "temp"
LOGS_DIR = APP_DATA_DIR / "logs"
HISTORY_DIR = APP_DATA_DIR / "history"
EXPORT_DIR = APP_DATA_DIR / "exports"

# 7. Default User Paths
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / APP_NAME
DEFAULT_TEMP_DIR = Path(tempfile.gettempdir()) / "NexoraTemp"

def create_app_directories():
    """App စတင်ချိန်တွင် လိုအပ်သော AppData Folder များကို အလိုအလျောက် Create လုပ်ပေးမည်"""
    directories = [
        APP_DATA_DIR,        
        DOWNLOAD_DIR,        
        TEMP_DIR,
        LOGS_DIR,
        HISTORY_DIR,
        EXPORT_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)