from core.url.url_validator import is_valid_url
from core.url.url_detector import detect_url_type


class URLManager:
    def analyze(self, url: str) -> dict:
            """Main Entry Point: URL ကို စစ်ဆေးပြီး သင့်တော်သော Result ထုတ်ပေးမည်"""
            if not url:
                return {
                    "valid": False,
                    "error": "URL string is empty",
                    "type": None,
                    "url": url
                }

            cleaned_url = url.strip()

            # 1. Validation Check
            if not is_valid_url(cleaned_url):
                return {
                    "valid": False,
                    "error": "Invalid URL scheme or format",
                    "type": None,
                    "url": cleaned_url
                }

            # 2. Type Detection
            detection = detect_url_type(cleaned_url)

            return {
                "valid": True,
                "error": None,
                "type": detection["type"],
                "provider": detection["provider"],
                "url": cleaned_url
            }


