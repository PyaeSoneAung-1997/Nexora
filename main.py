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
    print("🚀 Initializing Nexora Engine...\n")

    # 1. Folders ဖန်တီးခြင်း
    create_app_directories()
    print("📁 System directories initialized.")

    # 2. Database Initialization
    db = DatabaseManager()
    print("💾 SQLite Database initialized successfully.")

    # 3. App Config Load လုပ်ခြင်း
    # config = AppConfig()
    # print("⚙️  App Settings Loaded.")

    # 4. Auth Manager & Credentials Test ပြုလုပ်ခြင်း
    auth_mgr = GoogleAuthManager(db_manager=db)
    active_accounts = auth_mgr.get_active_accounts()

    if active_accounts:
        print(f"\n🔑 Logged in Accounts ({len(active_accounts)}):")
        for acc in active_accounts:
            acc_id = acc["id"]
            email = acc["email"]
            
            # 🌟 ဒီနေရာမှာ get_credentials ကို စမ်းသပ် ခေါ်ယူသုံးစွဲပါသည် 🌟
            creds = auth_mgr.get_credentials(account_id=acc_id)
            
            if creds:
                print(f"   - [{acc_id}] {acc['name']} ({email}) -> Credentials Active & Valid ✅")
            else:
                print(f"   - [{acc_id}] {acc['name']} ({email}) -> Credentials Invalid / Token Missing ❌")
    else:
        print("\n🔒 No active accounts found. Starting Google Login Flow...")
        try:
            account = auth_mgr.login()
            print(f"✅ Login Successful for: {account['email']}")
        except Exception as e:
            print(f"❌ Login Failed or Cancelled: {e}")

    print("\n✅ Nexora Core Initialization Complete!\n")

    # 5. URL Check First
    manager = URLManager()
    result = manager.analyze("https://drive.google.com/file/d/12345/view")
    print(result)




if __name__ == "__main__":
    main()
