# main.py

from core.database.db_manager import DatabaseManager
from core.cloud.drive_scanner import DriveScanner
from core.cloud.drive_resolver import DriveResolver


def test_drive_modules():
    print("🚀 Initializing Database & Modules...")
    db = DatabaseManager()
    
    # 1. Database Table များ ရှိမရှိ/ဆောက်ပြီး မရှိ စစ်ဆေးမည်
    # (သင့် db_manager ထဲတွင် table creation logic ပါပြီးဖြစ်ရပါမည်)
    
    account_id = 1  # စမ်းသပ်မည့် Account ID (accounts table ထဲတွင် ရှိပြီးသား ဖြစ်ရပါမည်)

    # ------------------------------------------------------------------
    # TEST 1: DriveResolver စမ်းသပ်ခြင်း (Link သို့မဟုတ် ID ဖြင့် ဖတ်ခြင်း)
    # ------------------------------------------------------------------
    print("\n==========================================")
    print("📌 [TEST 1] DriveResolver Testing")
    print("==========================================")
    
    resolver = DriveResolver(db_manager=db)
    
    # စမ်းသပ်လိုသည့် Google Drive File/Folder Link သို့မဟုတ် ID ထည့်ပါ
    test_url_or_id = "1aBC123xyz_sample_id_or_url" 
    
    try:
        print(f"🔎 Resolving URL/ID: {test_url_or_id}")
        resolved_file = resolver.resolve(account_id=account_id, url_or_id=test_url_or_id, save_to_db=True)
        print("✅ Resolved & Saved to DB Successfully:")
        print(f"   - Name: {resolved_file['name']}")
        print(f"   - File ID: {resolved_file['file_id']}")
        print(f"   - MimeType: {resolved_file['mime_type']}")
        print(f"   - Size: {resolved_file['size']} bytes")
    except Exception as e:
        print(f"⚠️ Resolver Error (or Invalid Test ID): {e}")

    # ------------------------------------------------------------------
    # TEST 2: DriveScanner စမ်းသပ်ခြင်း (Location Route အလိုက် Scan ဖတ်ခြင်း)
    # ------------------------------------------------------------------
    print("\n==========================================")
    print("📌 [TEST 2] DriveScanner Testing")
    print("==========================================")
    
    scanner = DriveScanner(db_manager=db)

    try:
        # My Drive ကို စကန်ဖတ်ခြင်း
        print("\n▶️ Scanning 'drive/my-drive'...")
        scan_result = scanner.process_location(account_id=account_id, location="drive/my-drive")
        print("✅ My Drive Scan Completed:", scan_result)

    except Exception as e:
        print(f"❌ Scanner Error: {e}")

    # ------------------------------------------------------------------
    # TEST 3: Database ထဲ အချက်အလက်များ ဝင်မဝင် စစ်ဆေးခြင်း
    # ------------------------------------------------------------------
    print("\n==========================================")
    print("📌 [TEST 3] Verifying Database Records")
    print("==========================================")

    # 1. Drives Table စစ်မည်
    drives = db.fetch_all("SELECT id, account_id, drive_id, name, total_files, total_folders, total_size, status FROM drives")
    print(f"\n📂 [drives Table] (Total Records: {len(drives)}):")
    for d in drives:
        print(f"   - [{d['drive_id']}] {d['name']} | Files: {d['total_files']} | Folders: {d['total_folders']} | Size: {d['total_size']} bytes | Status: {d['status']}")

    # 2. Sync Jobs Table စစ်မည်
    jobs = db.fetch_all("SELECT id, drive_id, job_type, status, scanned_files, scanned_folders, started_at, completed_at FROM sync_jobs")
    print(f"\n🔄 [sync_jobs Table] (Total Records: {len(jobs)}):")
    for j in jobs:
        print(f"   - Job #{j['id']} | Drive: {j['drive_id']} | Status: {j['status']} | Scanned Files: {j['scanned_files']} | Folders: {j['scanned_folders']}")

    # 3. Drive Files Table စစ်မည် (ပထမဆုံး ၅ ခု)
    files = db.fetch_all("SELECT id, drive_id, file_id, name, mime_type, size, is_folder, created_at, modified_time FROM drive_files LIMIT 5")
    print(f"\n📄 [drive_files Table] (Showing top 5 files):")
    for f in files:
        file_type = "Folder" if f['is_folder'] else "File"
        print(f"   - [{file_type}] {f['name']} ({f['file_id']}) | Size: {f['size']} | Created: {f['created_at']} | Modified: {f['modified_time']}")


if __name__ == "__main__":
    test_drive_modules()