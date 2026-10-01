from core.database.db_manager import DatabaseManager

class DriveRepositroy:

    def __init__(self, db_manager:DatabaseManager):
        self.db_manager = db_manager

    def create(
            self,
            account_id: int,
            drive_id: str,
            name: str,
            type: str,
            sync_tocken: str | None,
            total_files: int,
            total_folders: int,
            total_size: int,
            last_scanned: str,
            status: str ,
    ) -> int:

        query = """
        INSERT INTO drives (
            account_id,
            drive_id,
            name,
            type,
            sync_token,
            total_files,
            total_folders,
            total_size,
            last_scanned,
            status
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """

        return self.db_manager.execute_query(
            query,
            (
                account_id,
                drive_id,
                name,
                type,
                sync_tocken,
                total_files,
                total_folders,
                total_size,
                last_scanned,
                status
            )
        )