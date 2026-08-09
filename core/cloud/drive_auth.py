import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config.paths import CLIENT_SECRETS_FILE, APP_DATA_DIR

# Google Drive Read-only Access Scope
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
TOKEN_FILE = APP_DATA_DIR / "token.json"


class GoogleAuthManager:
    def __init__(self):
        self.creds = None
        self.service = None

    def get_credentials(self) -> Credentials:
        """Token ရှိမရှိ စစ်ဆေးပြီး လိုအပ်ပါက Refresh သို့မဟုတ် Browser Authentication ပြုလုပ်မည်"""
        # 1. သိမ်းထားပြီးသား Token ရှိပါက ဖတ်ယူမည်
        if TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        # 2. Token မရှိပါက သို့မဟုတ် Expire ဖြစ်သွားပါက ပြန်လည် ရယူမည်
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh Token ဖြင့် Token အသစ်ပြန်တောင်းမည်
                self.creds.refresh(Request())
            else:
                # Token လုံးဝမရှိပါက client_secrets.json ဖြင့် Browser စာမျက်နှာ ဖွင့်မည်
                if not CLIENT_SECRETS_FILE.exists():
                    raise FileNotFoundError(
                        f"Missing client_secrets.json at {CLIENT_SECRETS_FILE}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CLIENT_SECRETS_FILE), SCOPES
                )
                # Desktop App များအတွက် Local Server Flow သုံးမည်
                self.creds = flow.run_local_server(port=0)

            # ရရှိလာသော Token ကို သိုလှောင်ထားမည်
            with open(TOKEN_FILE, "w") as token_out:
                token_out.write(self.creds.to_json())

        return self.creds

    def get_drive_service(self):
        """Google Drive API Client Service ကို ပြန်ထုတ်ပေးမည်"""
        if not self.service:
            creds = self.get_credentials()
            self.service = build("drive", "v3", credentials=creds)
        return self.service

    def logout(self) -> bool:
        """သိမ်းထားသော Token ကို ဖျက်ပစ်ပြီး Logout ပြုလုပ်မည်"""
        if TOKEN_FILE.exists():
            os.remove(TOKEN_FILE)
            self.creds = None
            self.service = None
            return True
        return False

# UI သို့မဟုတ် အခြားနေရာများမှ အလွယ်တကူ ခေါ်သုံးရန် Helper Function
def logout_user() -> bool:
    """Google Account Logout ပြုလုပ်မည့် Helper Function"""
    auth_manager = GoogleAuthManager()
    return auth_manager.logout()