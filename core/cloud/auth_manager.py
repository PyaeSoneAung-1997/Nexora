# core/cloud/auth_manager.py

import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config.paths import APP_DATA_DIR, CLIENT_SECRETS_FILE
from config.constants import GOOGLE_SCOPES
from core.database.db_manager import DatabaseManager


class GoogleAuthManager:
    """Google OAuth 2.0 Authentication & Account Session Manager"""

    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
        self.tokens_dir = APP_DATA_DIR / "tokens"
        self.tokens_dir.mkdir(parents=True, exist_ok=True)

    def login(self) -> dict | None:
        """
        Google OAuth Login Flow ကို စတင်ပြီး Token သိမ်းဆည်းကာ DB သို့ Account သွင်းမည်
        """
        if not CLIENT_SECRETS_FILE.exists():
            raise FileNotFoundError(
                f"Client secrets file not found at '{CLIENT_SECRETS_FILE}'. "
                "Please place your client_secret.json file in the config folder."
            )

        # 1. OAuth Local Server Flow စတင်မည်
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE), 
            scopes=GOOGLE_SCOPES
        )
        creds = flow.run_local_server(port=0)

        # 2. Login ဝင်ထားသော အကောင့်၏ Profile (Email & Display Name) ကို တောင်းယူမည်
        service = build("drive", "v3", credentials=creds)
        about_info = service.about().get(fields="user").execute()
        user_info = about_info.get("user", {})

        email = user_info.get("emailAddress")
        name = user_info.get("displayName", email)

        if not email:
            raise ValueError("Failed to retrieve user email from Google account.")

        # 3. Token ကို JSON ဖိုင်အဖြစ် သီးသန့် Save မည်
        token_file_path = self.tokens_dir / f"{email}.json"
        with open(token_file_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

        # 4. Database `accounts` ဇယားထဲသို့ Insert/Update ပြုလုပ်မည်
        query = """
            INSERT INTO accounts (email, name, token_path, status, last_used_at)
            VALUES (?, ?, ?, 'active', datetime('now', 'localtime'))
            ON CONFLICT(email) DO UPDATE SET
                name = excluded.name,
                token_path = excluded.token_path,
                status = 'active',
                last_used_at = datetime('now', 'localtime');
        """
        account_id = self.db.execute_query(query, (email, name, str(token_file_path)))

        return self.get_account_by_email(email)

    def get_credentials(self, account_id: int) -> Credentials | None:
        """
        Account ID အလိုက် Credentials ကို ဖတ်ယူမည်။ Expired ဖြစ်ပါက Auto-Refresh လုပ်ပေးမည်။
        """
        account = self.db.fetch_one("SELECT * FROM accounts WHERE id = ?", (account_id,))
        if not account or account["status"] != "active":
            return None

        token_path = Path(account["token_path"])
        if not token_path.exists():
            # Token ဖိုင် မရှိတော့ပါက status ကို logged_out ဟု ပြောင်းမည်
            self.db.execute_query(
                "UPDATE accounts SET status = 'logged_out' WHERE id = ?", (account_id,)
            )
            return None

        creds = Credentials.from_authorized_user_file(str(token_path), scopes=GOOGLE_SCOPES)

        # Token သက်တမ်း ကုန်နေပါက Auto-Refresh ပြုလုပ်မည်
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Updated Token ကို JSON ထဲ ပြန်ရေးမည်
            with open(token_path, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

        # Last Used Time ကို DB ထဲ Update လုပ်မည်
        self.db.execute_query(
            "UPDATE accounts SET last_used_at = CURRENT_TIMESTAMP WHERE id = ?", (account_id,)
        )

        return creds

    def logout(self, account_id: int) -> bool:
        """
        Account တစ်ခုကို Logout လုပ်မည် (Token file ဖျက်ပြီး Status ပြောင်းမည်)
        """
        account = self.db.fetch_one("SELECT token_path FROM accounts WHERE id = ?", (account_id,))
        if not account:
            return False

        token_path = Path(account["token_path"])
        if token_path.exists():
            try:
                os.remove(token_path)
            except OSError:
                pass

        self.db.execute_query(
            "UPDATE accounts SET status = 'logged_out' WHERE id = ?", (account_id,)
        )
        return True

    def get_active_accounts(self) -> list[dict]:
        """Active ဖြစ်နေသော Account များအားလုံးကို ထုတ်ယူမည်"""
        return self.db.fetch_all("SELECT * FROM accounts WHERE status = 'active'")

    def get_account_by_email(self, email: str) -> dict | None:
        """Email ဖြင့် Account အချက်အလက် ရှာယူမည်"""
        return self.db.fetch_one("SELECT * FROM accounts WHERE email = ?", (email,))