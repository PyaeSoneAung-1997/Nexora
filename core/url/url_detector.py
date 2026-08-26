from urllib.parse import urlparse, parse_qs


def detect_url_type(url: str) -> dict:
    """URL အမျိုးအစားကို ခွဲခြားပြီး Type နှင့် Extra Data ပြန်ထုတ်ပေးမည်"""
    url_lower = url.lower()
    domain = urlparse(url).netloc.lower()

    # 1. Google Drive Detection
    if "drive.google.com" in domain or "docs.google.com" in domain:
        return {
            "type": "google_drive",
            "provider": "Google Drive"
        }

    # 2. Direct File Extension Detection
    file_extensions = (
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".mp4", ".mkv", ".avi", ".mp3",".bin",
        ".pdf", ".iso", ".exe", ".msi", ".dmg"
    )

    # URL Path (or Query String) ထဲမှာ Extension ပါမပါ စစ်ဆေးခြင်း
    path = urlparse(url).path.lower()
    if any(path.endswith(ext) for ext in file_extensions):
        return {
            "type": "direct_file",
            "provider": "Direct Link"
        }

    # 3. Other Web Link / Webpage
    return {
        "type": "website",
        "provider": "Web Link"
    }