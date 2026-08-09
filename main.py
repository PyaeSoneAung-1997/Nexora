# main.py
from config import (
    create_app_directories, 
    APP_DATA_DIR,
    APP_NAME,
    APP_VERSION)
from config import AppConfig
from core.database.db_manager import DatabaseManager
from core.url import URLManager
from core.cloud.auth_manager import GoogleAuthManager

def main():
# Step-1
    # Base AppData Folders ဖန်တီးခြင်း
    # create_app_directories()
    # print(f"App name:{APP_NAME}\nApp version:{APP_VERSION} \nApp Data Dir:{APP_DATA_DIR}")
    # config = AppConfig()
    # print("⚙️  App Settings Loaded:")
    # print(f"   - Download Path: {config.download_path}")
    # print(f"   - Temp Path    : {config.temp_path}")
    # print(f"   - Max Downloads: {config.max_concurrent}")
    # print(f"   - Theme        : {config.theme}")
    
    db = DatabaseManager()
    settings_count = db.fetch_one("SELECT COUNT(*) as count FROM app_settings")["count"]
    print(f"📊 Total settings seeded in Database: {settings_count}")

    print("\n✅ Nexora Core Initialization Complete!\n")

    auth_mgr = GoogleAuthManager(db_manager=db)
    active_accounts = auth_mgr.get_active_accounts()

    if active_accounts:
        print(f"🔑 Logged in Accounts ({len(active_accounts)}):")
        for acc in active_accounts:
            print(f"   - {acc['name']} ({acc['email']}) [Status: {acc['status']}]")
    else:
        print("🔒 No active accounts found. Starting Google Login Flow...")
        try:
            # Login မဝင်ရသေးပါက Browser ဖွင့်ပြီး Login တောင်းမည်
            account = auth_mgr.login()
            print(f"✅ Login Successful!")
            print(f"   - Account Name : {account['name']}")
            print(f"   - Account Email: {account['email']}")
            print(f"   - Token Stored : {account['token_path']}")
        except FileNotFoundError as e:
            print(f"⚠️  Login Warning: {e}")
            print("   (Please add 'client_secret.json' into the config folder to log in)")
        except Exception as e:
            print(f"❌ Login Failed: {e}")

    print("\n✅ Nexora Core Initialization Complete!\n")
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