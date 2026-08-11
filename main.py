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
from core.cloud.drive_resolver import DriveResolver
from core.cloud.drive_scanner import DriveScanner

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
    # url = "https://drive.google.com/drive/folders/16J1isPtoHQJIOWfbRD3rfmYh7MhTIKw6"
    # url = "https://drive.google.com/drive/my-drive"
    url = "https://drive.google.com/drive/shared-drives"
    # url = "https://drive.google.com/drive/folders/0AO8hnuAAF4SoUk9PVA"
    
    manager = URLManager()
    result = manager.analyze(url)
    # print(result)

    resolv = DriveResolver()
    res     = resolv.resolve(acc_id,url)

    print(res)
    scanner = DriveScanner()
    list = scanner.list_shared_drives(acc_id)
    print(list[0]['id'])
    scan_info = scanner.scan_single_shared_drive(acc_id, list[0]['id'], list[0]['name'])
    print(scan_info)



if __name__ == "__main__":
    main()
