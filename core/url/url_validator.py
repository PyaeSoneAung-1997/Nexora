from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """URL ရဲ့ Syntax နှင့် Scheme (http/https) မှန်မမှန် စစ်ဆေးပေးမည်"""
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url.strip())
        return all([
            result.scheme in ["http", "https"],
            result.netloc
        ])
    except Exception:
        return False