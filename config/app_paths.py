import os
import sys
import tempfile
from pathlib import Path

APP_NAME = "Nexora"

# 1. Base Directory (Bundled Read-Only Files)
# App ကို Python script (.py) အဖြစ် run ချိန် နှင့် PyInstaller (.exe) ထုတ်ပြီးချိန် ၂ မျိုးလုံးတွင် အလုပ်လုပ်ပါမည်
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Bundled Assets, Executables & Secrets
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STYLES_DIR = ASSETS_DIR / "styles"

ARIA2_DIR = BASE_DIR / "aria2"
ARIA2_PATH = ARIA2_DIR / "aria2c.exe"

CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"


# 2. System AppData Directory (Writeable Runtime Files)
# Windows: C:\Users\<User>\AppData\Roaming\Nexora\data
SYSTEM_APPDATA = os.getenv("APPDATA") or os.path.expanduser("~")
APP_DATA_DIR = Path(SYSTEM_APPDATA) / APP_NAME 
LOGS_DIR = APP_DATA_DIR / "logs"
TEMP_DIR = APP_DATA_DIR / "temp"
EXPORT_DIR = APP_DATA_DIR / "exports"

DATABASE_PATH = APP_DATA_DIR / "nexora.db"
DOWNLOAD_DIR  = APP_DATA_DIR / "downloads" 


DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / APP_NAME
DEFAULT_TEMP_DIR = Path(tempfile.gettempdir()) / "NexoraTemp"

def create_app_directories():
    """App စတင်ချိန်တွင် လိုအပ်သော AppData Folder များကို အလိုအလျောက် Create လုပ်ပေးမည်"""
    directories = [
        APP_DATA_DIR,
        LOGS_DIR,
        TEMP_DIR,
        EXPORT_DIR,
        DOWNLOAD_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)