from config.constants import DEFAULT_DOWNLOAD_PATH, DEFAULT_CONNECTIONS, DEFAULT_SPLIT

DEFAULT_SETTINGS = {
    "default_download_path": str(DEFAULT_DOWNLOAD_PATH),
    "max_concurrent_downloads": 3,
    "max_connections_per_file": DEFAULT_CONNECTIONS,
    "max_split_count": DEFAULT_SPLIT,
    "max_retries_per_item": 5,
    "auto_resume_on_startup": True,
    "theme": "dark",
    "notify_on_complete": True,
}