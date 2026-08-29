from core.database.db_manager import DatabaseManager

class ConfigManager:
    """Database app_settings ဇယားမှ Dynamic Settings များကို ဖတ်/ရေး ရန် Class"""
    def __init__(self, db_manager: DatabaseManager = None):
        self.db_manager = db_manager or DatabaseManager()

    def get(self, key: str, default: str = None) -> str:
        row = self.db_manager.fetch_one("SELECT value FROM app_settings WHERE key = ?", (key,))
        return row["value"] if row else default

    def set(self, key: str, value: str) -> None:
        self.db_manager.execute_query(
                "UPDATE app_settings SET value = ?, updated_at = datetime('now', 'localtime') WHERE key = ?",
                (str(value), key)
            )

    def get_category(self, category: str) -> dict:
        rows = self.db_manager.fetch_all("SELECT key, value FROM app_settings WHERE category = ?", (category,))
        return {row["key"]: row["value"] for row in rows}   