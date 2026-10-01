from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
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