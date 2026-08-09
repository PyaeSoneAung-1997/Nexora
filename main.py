# main.py
from config import (
    create_app_directories, 
    APP_DATA_DIR,
    APP_NAME,
    APP_VERSION)

from core.url import URLManager
from core.cloud.drive_auth import GoogleAuthManager, logout_user

def main():
# Step-1
    # Base AppData Folders ဖန်တီးခြင်း
    # create_app_directories()
    
    # print(f"App Name: {APP_NAME}")
    # print(f"App version: {APP_VERSION}")
    # print(f"Nexora Initialized Successfully!")
    # print(f"App Data Directory: {APP_DATA_DIR}")

#Step-2
    #Url Check First
    # manager = URLManager()
    # result = manager.analyze("https://drive.google.com/file/d/12345/view")
    # print(result)

#Step-3
    #Google Drive Connect
    # auth_manager = GoogleAuthManager()
    
    # try:
    #     # Token မရှိပါက Browser ပွင့်လာပြီး Login ဝင်ခိုင်းပါမည်
    #     service = auth_manager.get_drive_service()
    #     print("✅ Google Login Successful!")
    # except Exception as e:
    #     print(f"❌ Login Failed: {e}")


if __name__ == "__main__":
    main()
#Step-3
    #Token File Delete log out function call
    # if logout_user():
    #     print("🚪 Logged out successfully!")
    # else:
    #     print("⚠️ No active session found.")