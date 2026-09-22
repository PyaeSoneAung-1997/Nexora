# ============================================================
# Nexora - Application Config Manager
# Version: 1.0.0
# ============================================================

from typing import Mapping

from core.database.db_manager import DatabaseManager


class ConfigManager:
    """
    Database ရှိ app_settings table မှ
    Dynamic Application Settings များကို
    ဖတ် / ရေး / စီမံရန် အသုံးပြုသည်။

    ConfigManager သည် Database Layer နှင့်
    Application Configuration Layer ကြားရှိ
    Settings Access Layer ဖြစ်သည်။
    """

    def __init__(
        self,
        db_manager: DatabaseManager | None = None,
        default_settings: Mapping[str, tuple[str, str]] | None = None,
    ):
        # ----------------------------------------------------
        # Database
        # ----------------------------------------------------

        self.db_manager = db_manager or DatabaseManager()

        # ----------------------------------------------------
        # Default Settings
        #
        # {
        #     "setting_key": ("value", "category")
        # }
        # ----------------------------------------------------

        self.default_settings = default_settings or {}

        # ----------------------------------------------------
        # Make sure default settings exist in DB
        # ----------------------------------------------------

        self.initialize_defaults()

    # ========================================================
    # Initialize
    # ========================================================

    def initialize_defaults(self) -> None:
        """
        Default settings များကို app_settings table ထဲ
        မရှိသေးလျှင် ထည့်ပေးသည်။

        ရှိပြီးသား user settings များကို
        overwrite မလုပ်ပါ။
        """

        if not self.default_settings:
            return

        for key, setting in self.default_settings.items():
            value, category = setting

            self.db_manager.execute_query(
                """
                INSERT INTO app_settings
                    (key, value, category, updated_at)
                VALUES
                    (?, ?, ?, datetime('now', 'localtime'))
                ON CONFLICT(key) DO NOTHING
                """,
                (
                    key,
                    str(value),
                    category,
                ),
            )

    # ========================================================
    # Get
    # ========================================================

    def get(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        """
        Setting တစ်ခု၏ value ကို ပြန်ပေးသည်။

        Setting မရှိလျှင် default ကို ပြန်ပေးသည်။
        """

        row = self.db_manager.fetch_one(
            """
            SELECT value
            FROM app_settings
            WHERE key = ?
            """,
            (key,),
        )

        if row is None:
            return default

        return row["value"]

    # ========================================================
    # Set
    # ========================================================

    def set(
        self,
        key: str,
        value: str,
        category: str | None = None,
    ) -> None:
        """
        Setting value ကို Database ထဲသို့ သိမ်းသည်။

        Key ရှိပြီးသားဆိုရင် UPDATE လုပ်မည်။
        Key မရှိသေးရင် INSERT လုပ်မည်။

        category မပေးထားပါက
        ရှိပြီးသား category ကို မပြောင်းပါ။
        """

        existing = self.db_manager.fetch_one(
            """
            SELECT key, category
            FROM app_settings
            WHERE key = ?
            """,
            (key,),
        )

        if existing:
            self.db_manager.execute_query(
                """
                UPDATE app_settings
                SET
                    value = ?,
                    updated_at = datetime('now', 'localtime')
                WHERE key = ?
                """,
                (
                    str(value),
                    key,
                ),
            )

            return

        # ----------------------------------------------------
        # New Setting
        # ----------------------------------------------------

        setting_category = category or "general"

        self.db_manager.execute_query(
            """
            INSERT INTO app_settings
                (key, value, category, updated_at)
            VALUES
                (?, ?, ?, datetime('now', 'localtime'))
            """,
            (
                key,
                str(value),
                setting_category,
            ),
        )

    # ========================================================
    # Get Category
    # ========================================================

    def get_category(self, category: str) -> dict[str, str]:
        """
        Category တစ်ခုအောက်ရှိ Settings အားလုံးကို
        Dictionary အဖြစ် ပြန်ပေးသည်။
        """

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

    # ========================================================
    # Delete
    # ========================================================

    def delete(self, key: str) -> None:
        """
        Setting တစ်ခုကို Database မှ ဖျက်သည်။
        """

        self.db_manager.execute_query(
            """
            DELETE FROM app_settings
            WHERE key = ?
            """,
            (key,),
        )

    # ========================================================
    # Exists
    # ========================================================

    def exists(self, key: str) -> bool:
        """
        Setting key တစ်ခု Database ထဲတွင် ရှိ/မရှိ စစ်သည်။
        """

        row = self.db_manager.fetch_one(
            """
            SELECT 1
            FROM app_settings
            WHERE key = ?
            LIMIT 1
            """,
            (key,),
        )

        return row is not None

    # ========================================================
    # Get All
    # ========================================================

    def get_all(self) -> dict[str, str]:
        """
        Application Settings အားလုံးကို
        Dictionary အဖြစ် ပြန်ပေးသည်။
        """

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

    # ========================================================
    # Reset
    # ========================================================

    def reset(self, key: str) -> None:
        """
        Setting တစ်ခုကို Default Value သို့ ပြန်ထားသည်။

        Default setting မရှိပါက ဘာမှမလုပ်ပါ။
        """

        if key not in self.default_settings:
            return

        value, category = self.default_settings[key]

        self.set(
            key=key,
            value=str(value),
            category=category,
        )

    # ========================================================
    # Reset All
    # ========================================================

    def reset_all(self) -> None:
        """
        Application Settings အားလုံးကို
        Default Values သို့ ပြန်ထားသည်။
        """

        for key, setting in self.default_settings.items():
            value, category = setting

            self.set(
                key=key,
                value=str(value),
                category=category,
            )
