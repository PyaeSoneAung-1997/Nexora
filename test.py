import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from core.cloud.auth_manager import GoogleAuthManager
from core.database.db_manager import DatabaseManager

class DriveResolver:
    """Google Drive Link/ID များကို စစ်ဆေးပြီး Metadata ထုတ်ယူကာ DB သို့ သိမ်းဆည်းပေးမည့် Service"""

    def __init__(self, auth_manager: GoogleAuthManager = None, db_manager: DatabaseManager = None):
        self.auth_mgr = auth_manager or GoogleAuthManager()
        self.db = db_manager or DatabaseManager()

    @staticmethod
    def extract_id(url_or_id: str) -> str | None:
            """Google Drive URL သို့မဟုတ် Raw ID ထဲမှ Target ID ကို သီးသန့် ထုတ်ယူမည်"""
            if not url_or_id:
                return None

            url_or_id = url_or_id.strip()

            # 1. Folder Link စစ်မည် (/folders/xxx)
            folder_match = re.search(r"/folders/([\w-]+)", url_or_id)
            if folder_match:
                return folder_match.group(1)

            # 2. File Link စစ်မည် (/file/d/xxx)
            file_match = re.search(r"/file/d/([\w-]+)", url_or_id)
            if file_match:
                return file_match.group(1)

            # 3. ID = parameter ပါသော Link (e.g., open?id=xxx)
            id_param_match = re.search(r"[?&]id=([\w-]+)", url_or_id)
            if id_param_match:
                return id_param_match.group(1)

            # 4. Raw ID သီးသန့် ရိုက်ထည့်ထားခြင်း (အနည်းဆုံး ၂၅ လုံးနှင့်အထက်)
            if re.fullmatch(r"[\w-]{25,}", url_or_id):
                return url_or_id

            return None

    # def resolve(self, account_id: int, url_or_id: str, save_to_db: bool = True) -> dict:
    def resolve(self, account_id: int, url_or_id: str) -> dict:
            """
            Drive ID ကို API ခေါ်ပြီး File/Folder Metadata အချက်အလက်များ တောင်းယူမည်။
            `save_to_db=True` ပါပါက `drive_files` Table ထဲသို့ တိုက်ရိုက် သိမ်းဆည်းပေးမည်။
            """
            

            creds = self.auth_mgr.get_credentials(account_id)
            if not creds:
                raise ValueError(f"No active session found for Account ID: {account_id}")

            service = build("drive", "v3", credentials=creds)

            check_url = url.lower()
            if "/home" in check_url:
                return {
                                        "type": "home",
                                        "action":"all_drives",
            
                                        "id": None,
                                        "name": "Drive Home",
            
                                        "drive_type":None,
                                        "drive_id": None,
            
                                        "mime_type": None,
                                        "is_folder": 0
                                    }
            if "/my-drive" in check_url or "my_drive" in check_url:
                                return {
                                                "type": "home",
                                                "action":"all_drives",
                        
                                                "id": None,
                                                "name": "Drive Home",
                        
                                                "drive_type":None,
                                                "drive_id": None,
                        
                                                "mime_type": None,
                                                "is_folder": 0
                                        }     
            if "/shared-drives"  in check_url:
                            return {
                                              "type": "home",
                                              "action":"all_drives",
                      
                                              "id": None,
                                              "name": "Drive Home",
                      
                                              "drive_type":None,
                                              "drive_id": None,
                      
                                              "mime_type": None,
                                              "is_folder": 0
                                    }     

                      # Google Drive API မှတစ်ဆင့် Metadata တောင်းယူမည်
            target_id = self.extract_id(url_or_id)
            if not target_id:
                    raise ValueError("Invalid Google Drive Link or ID format.")
            try:
                # Google Drive API မှတစ်ဆင့် Metadata တောင်းယူမည်
                f = service.files().get(
                    fileId=target_id,
                    fields="id, name, mimeType, size, parents, driveId, webViewLink, md5Checksum, trashed, createdTime, modifiedTime",
                    supportsAllDrives=True
                ).execute()

                mime_type = f.get("mimeType", "")
                is_folder = 1 if mime_type == "application/vnd.google-apps.folder" else 0
                is_workspace = 1 if (mime_type.startswith("application/vnd.google-apps.") and not is_folder) else 0
                parent_id = f.get("parents", [None])[0]
                drive_id = f.get("driveId", "root") # Shared Drive မဟုတ်ပါက 'root' ဟု သတ်မှတ်မည်

                result_data = {
                    "account_id": account_id,
                    "drive_id": drive_id,
                    "file_id": f["id"],
                    "parent_id": parent_id,
                    "name": f["name"],
                    "mime_type": mime_type,
                    "size": int(f.get("size", 0)),
                    "is_folder": is_folder,
                    "is_workspace_file": is_workspace,
                    "relative_path": f["name"],
                    "md5_checksum": f.get("md5Checksum"),
                    "web_view_link": f.get("webViewLink"),
                    "trashed": 1 if f.get("trashed") else 0,
                    "created_at": f.get("createdTime"),
                    "modified_time": f.get("modifiedTime")
                }
                return result_data
       
            except HttpError as e:
                   if e.resp.status == 404:
                       raise FileNotFoundError("Drive item not found or permission denied.")
                   raise Exception(f"Google Drive API Error: {e.reason}")
            
if __name__  ==  "__main__":
    id = "1"
    url = "https://drive.google.com/drive/folders/16J1isPtoHQJIOWfbRD3rfmYh7MhTIKw6"
    # url = "https://drive.google.com/drive/my-drive"
    # url = "https://drive.google.com/drive/shared-drives"

    manager = DriveResolver()
    result = manager.resolve(id ,url)
    print(result)