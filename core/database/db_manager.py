# ============================================================
# Nexora - Database Manager
# Version: 1.0.0
# ============================================================

from pathlib import Path
from typing import Any, Sequence

from config.app_paths import DATABASE_PATH
from core.database.connection import DatabaseConnection
from core.database.schema import CREATE_SCHEMA_SQL


class DatabaseManager:
    
    def __init__(
        self,
        database_path: str | Path = DATABASE_PATH,
        initialize: bool = True,
    ):
        self.database = DatabaseConnection(database_path)
        self.connection = self.database.connect()

        if initialize:
            self.initialize_schema()

    def initialize_schema(self) -> None:

        self.connection.executescript(CREATE_SCHEMA_SQL)
        self.connection.commit()

    # Execute Query

    def execute_query(
        self,
        query: str,
        parameters: Sequence[Any] = (),
    ) -> int:
      
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, parameters)
            self.connection.commit()

            return cursor.rowcount

        except Exception:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    # Execute Many

    def execute_many(
        self,
        query: str,
        parameters: Sequence[Sequence[Any]],
    ) -> None:
      
        cursor = self.connection.cursor()

        try:
            cursor.executemany(query, parameters)
            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    # Fetch One

    def fetch_one(
        self,
        query: str,
        parameters: Sequence[Any] = (),
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, parameters)
            return cursor.fetchone()

        finally:
            cursor.close()

    # Fetch All

    def fetch_all(
        self,
        query: str,
        parameters: Sequence[Any] = (),
    ):

        cursor = self.connection.cursor()

        try:
            cursor.execute(query, parameters)
            return cursor.fetchall()

        finally:
            cursor.close()

    # Execute Script

    def execute_script(
        self,
        script: str,
    ) -> None:
        try:
            self.connection.executescript(script)
            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise

    # Transaction

    def begin(self) -> None:
        self.connection.execute("BEGIN")

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    # Close

    def close(self) -> None:
        self.database.close()

    # Context Manager

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:

        if exc_type is not None:
            self.rollback()

        self.close()
