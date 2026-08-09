CREATE_SCHEMA_SQL = """
-- 1. ACCOUNTS
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    token_path TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at DATETIME
);

-- 2. DRIVES
CREATE TABLE IF NOT EXISTS drives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    drive_id VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    sync_token TEXT,
    total_files INTEGER DEFAULT 0,
    total_folders INTEGER DEFAULT 0,
    total_size BIGINT DEFAULT 0,
    last_scanned DATETIME,
    status VARCHAR(50) DEFAULT 'idle',
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 3. DRIVE_FILES
CREATE TABLE IF NOT EXISTS drive_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    drive_id VARCHAR(255) NOT NULL,
    file_id VARCHAR(255) NOT NULL UNIQUE,
    parent_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(255),
    size BIGINT DEFAULT 0,
    is_folder BOOLEAN DEFAULT 0,
    is_workspace_file BOOLEAN DEFAULT 0,
    relative_path TEXT NOT NULL,
    md5_checksum VARCHAR(64),
    web_view_link TEXT,
    trashed BOOLEAN DEFAULT 0,
    created_at DATETIME,
    modified_time DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 4. SYNC_JOBS
CREATE TABLE IF NOT EXISTS sync_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    drive_id VARCHAR(255) NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'queued',
    next_page_token TEXT,
    scanned_files INTEGER DEFAULT 0,
    scanned_folders INTEGER DEFAULT 0,
    error_message TEXT,
    started_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 5. DOWNLOAD_QUEUES
CREATE TABLE IF NOT EXISTS download_queues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    total_files INTEGER DEFAULT 0,
    completed_files INTEGER DEFAULT 0,
    total_bytes BIGINT DEFAULT 0,
    downloaded_bytes BIGINT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'queued',
    scheduled_start_at DATETIME,
    scheduled_stop_at DATETIME,
    auto_shutdown BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 6. DOWNLOAD_ITEMS
CREATE TABLE IF NOT EXISTS download_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_id INTEGER NOT NULL,
    drive_file_id INTEGER NOT NULL,
    destination_path TEXT NOT NULL,
    temp_path TEXT NOT NULL,
    export_mime_type VARCHAR(255),
    total_size BIGINT DEFAULT 0,
    downloaded_bytes BIGINT DEFAULT 0,
    order_index INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'queued',
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (queue_id) REFERENCES download_queues(id) ON DELETE CASCADE,
    FOREIGN KEY (drive_file_id) REFERENCES drive_files(id) ON DELETE CASCADE
);

-- 7. DOWNLOAD_HISTORY
CREATE TABLE IF NOT EXISTS download_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    file_id VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(255),
    file_size BIGINT DEFAULT 0,
    avg_speed BIGINT DEFAULT 0,
    duration_seconds INTEGER DEFAULT 0,
    destination_path TEXT NOT NULL,
    md5_checksum VARCHAR(64),
    queue_title VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    started_at DATETIME,
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 8. APP_SETTINGS
CREATE TABLE IF NOT EXISTS app_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(255) NOT NULL UNIQUE,
    value TEXT,
    category VARCHAR(100),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_files_parent ON drive_files(parent_id);
CREATE INDEX IF NOT EXISTS idx_files_drive ON drive_files(drive_id);
CREATE INDEX IF NOT EXISTS idx_files_path ON drive_files(relative_path);
CREATE INDEX IF NOT EXISTS idx_download_items_queue ON download_items(queue_id, order_index);
CREATE INDEX IF NOT EXISTS idx_download_items_status ON download_items(status);
CREATE INDEX IF NOT EXISTS idx_history_account ON download_history(account_id);
CREATE INDEX IF NOT EXISTS idx_history_status ON download_history(status);
"""