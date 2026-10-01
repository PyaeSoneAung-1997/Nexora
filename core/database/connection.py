# ============================================================
# Nexora - Database Connection
# Version: 1.0.0                                         
# ============================================================

import sqlite3
from pathlib import Path


class DatabaseConnection:

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.connection: sqlite3.Connection | None = None

    # Connect
    def connect(self) -> sqlite3.Connection:

        if self.connection is not None:
            return self.connection

        # Database directory မရှိသေးရင် create လုပ်မယ်
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            str(self.database_path)
        )

        # Dictionary-style row access
        self.connection.row_factory = sqlite3.Row

        # SQLite Configuration
        # Foreign Key support
        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        # Write-Ahead Logging
        self.connection.execute(
            "PRAGMA journal_mode = WAL"
        )

        return self.connection

    # Close
    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Context Manager
    def __enter__(self) -> sqlite3.Connection:
        return self.connect()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.close()

