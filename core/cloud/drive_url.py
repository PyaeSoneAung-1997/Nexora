import re

def extract_drive_id(url: str):
    """Google Drive URL ထဲမှ File ID / Folder ID / Shared Drive ID ကို ဆွဲထုတ်ပေးမည်"""
    if not url or not isinstance(url, str):
        return None

    patterns = [
        r"/folders/([a-zA-Z0-9_-]+)",
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)",
        r"/drives/([a-zA-Z0-9_-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
            
    return None