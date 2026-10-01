# ============================================================
# Nexora - Database Initialization Test
# ============================================================

from pathlib import Path
import sqlite3

from core.database.db_manager import DatabaseManager
from config.app_config_manager import ConfigManager
from config.app_config import AppConfig

TEST_DB_PATH = Path("tests/test_nexora.db")

DEFAULT_SETTINGS = {
    "theme" : ("dark", "ui"),
    "speed_limit_kbps": ("0", "network")
}
def main():
    # --------------------------------------------------------
    # Test DB ရှိပြီးသားဆို ဖျက်မယ်
    # --------------------------------------------------------

    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

    # --------------------------------------------------------
    # Database Create + Schema Initialize
    # --------------------------------------------------------

    db = DatabaseManager(
        database_path=TEST_DB_PATH
    )

    print("Database created successfully.")
    print(f"Database path: {TEST_DB_PATH.resolve()}")

    config = ConfigManager(db_manager=db)
    App = AppConfig(config)


    print("\n1. Get Settings")

    print(
        "theme:",
        config.get("theme")
    )
    print(config.get_all())

    # config  = AppConfig()

    print(App.download_path)
    # --------------------------------------------------------
    # Check Tables
    # --------------------------------------------------------

    rows = db.fetch_all(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    print("\nTables:")

    for row in rows:
        print(f" - {row['name']}")

    # --------------------------------------------------------
    # Check Expected Tables
    # --------------------------------------------------------

    expected_tables = {
        "accounts",
        "drives",
        "drive_files",
        "sync_jobs",
        "download_queues",
        "download_items",
        "downloads",
        "download_history",
        "app_settings",
    }

    actual_tables = {
        row["name"]
        for row in rows
    }

    missing_tables = expected_tables - actual_tables

    if missing_tables:
        print("\nERROR:")
        print("Missing tables:")

        for table in sorted(missing_tables):
            print(f" - {table}")

    else:
        print("\nAll expected tables created successfully.")

    # --------------------------------------------------------
    # Close
    # --------------------------------------------------------

    db.close()

    print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
