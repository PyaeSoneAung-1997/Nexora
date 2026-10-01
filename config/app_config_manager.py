# ============================================================
# Nexora - Application Config Manager
# Version: 1.0.0
# ============================================================

from collections.abc import Mapping
from typing import overload

from config.app_constants import DEFAULT_APP_SETTINGS
from core.database.db_manager import DatabaseManager

class ConfigManager:

    def __init__(
        self,
        db_manager: DatabaseManager | None = None,
        default_settings: Mapping[str, tuple[str, str]] | None = None,
    ):
      
        self.db_manager = db_manager or DatabaseManager()

        settings = (
            default_settings
            if default_settings is not None
            else DEFAULT_APP_SETTINGS
        )

        self.initialize_defaults(settings)

# Initialize
    def initialize_defaults(
            self,
            default_settings: Mapping[str, tuple[str,str]],
        ) -> None:

        query = """
                INSERT INTO app_settings
                    (key,value,category)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO NOTHING
        """

        parameters = [
            (key,value, category)
            for key, (value, category)
            in default_settings.items()
        ]

        if parameters:
            self.db_manager.execute_many(
                query,
                parameters,
            )

# Get
    @overload
    def get(
        self,
        key: str,
    ) -> str | None:
          ...

    @overload
    def get(
        self,
        key: str,
        default:str,
    ) -> str:
        ...

    def get(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:  

        row = self.db_manager.fetch_one(
            """
            SELECT value
            FROM app_settings
            WHERE key = ?
            """,
            (key,),
        )

        if row is not None:
            return row["value"]

        return default

# Set

    def set(
        self,
        key: str,
        value: str,
        category: str = "general",
    ) -> None:
        
        self.db_manager.execute_query(
                """
                INSERT INTO app_settings
                    (key,value,category)
                VALUES(?,?,?)

                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    categoty = excluded.category,
                    updated_at = datetime('now')
                """,
                (   
                    key,
                    str(value),
                    category,
                ),
            )

# Get Category
    
    def get_category(
            self, 
            category: str
    ) -> dict[str, str]:
      

        rows = self.db_manager.fetch_all(
            """
            SELECT key, value
            FROM app_settings
            WHERE category = ?
            ORDER BY key
            """,
            (category,),
        )

        return {
            row["key"]: row["value"]
            for row in rows
        }

# Exists
    def exists(
            self,
            key: str,
    ) -> bool:

        row = self.db_manager.fetch_one(
            """
            SELECT 1
            FROM app_settings
            WHERE key = ?
            LIMIT = 1
            """,
            (key,),
        )

        return row is not None

 # Delete
    def delete(
            self,
              key: str
    ) -> None:
        self.db_manager.execute_query(
            """
            DELETE FROM app_settings
            WHERE key = ?
            """,
            (key,),
        )

# Get All
    def get_all(
            self
    ) -> dict[str, str]:

        rows = self.db_manager.fetch_all(
            """
            SELECT key, value
            FROM app_settings
            ORDER BY key
            """
        )

        return {
            row["key"]: row["value"]
            for row in rows
        }

# Reset
    def reset(
            self, 
            key: str,
            default_settings: Mapping[str, tuple[str, str]],
    ) -> None:

        setting = default_settings.get(key)

        if setting is None:
            return

        value, category = setting
        self.set(
            key=key,
            value=str(value),
            category=category,
        )

# Reset All
    def reset_all(
            self,
            default_settings: Mapping[str, tuple[str,str]]
        ) -> None:

        for key, (value, category) in default_settings.items():
            
            self.set(
                key=key,
                value=value,
                category=category,

            )
