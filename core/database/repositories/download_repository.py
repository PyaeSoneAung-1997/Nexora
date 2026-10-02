from core.database.db_manager import DatabaseManager
from core.database.repositories.base_repository import BaseRepository

class DownloadRepository(BaseRepository):

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(
            db_manager,
            "downloads"
        )

    #1
    def create(
        self,
        url: str,
        url_type: str,
        title: str | None = None,
        file_name: str | None = None,
        destination_path: str | None = None
    ) -> int:
        # print("Repo")
        query = """
        INSERT INTO downloads(
            url,
            url_type,
            title,
            file_name,
            destination_path
        )
        VALUES (?,?,?,?,?)
        """

        return self.db_manager.execute_query(
            query,
            (
                url,
                url_type,
                title,
                file_name,
                destination_path
            )
        )

    #2
    def update_aria2_gid(
        self,
        download_id:int,
        aria2_gid:str
    ) -> None:

        query = """
        UPDATE downloads
        SET aria2_gid = ?
        WHERE id = ?
        """

        self.db_manager.execute_query(
            query,
            (
                aria2_gid,
                download_id    
            )
        )

    #3
    def update_status(
            self,
            download_id: int,
            status: str
    ) -> None:

        query = """
        UPDATE downloads
        SET Status = ?
        WHERE id = ?
        """

        self.db_manager.execute_query(
            query,
            (
                status,
                download_id
            )
        )

    #4
    def update_progress(
                self,
                download_id: int,
                downloaded_bytes: int,
                total_size: int,
                progress: int,
                speed: int,
                status:str
        ) -> None:
    
            query = """
            UPDATE downloads
            SET 
                downloaded_bytes = ?,
                total_size = ?,
                progress = ?,
                speed = ?, 
                status = ?
            WHERE id = ?
            """
    
            self.db_manager.execute_query(
                query,
                (
                    downloaded_bytes,
                    total_size,
                    progress,
                    speed,
                    status,
                    download_id
                )
            )

    #5
    def update_started_at(
                self,
                download_id: int,
                started_at: str
        ) -> None:
    
            query = """
            UPDATE downloads
            SET started_at = ?
            WHERE id = ?
            """
    
            self.db_manager.execute_query(
                query,
                (
                    started_at,
                    download_id
                )
            )

    #6
    def update_completed_at(
                self,
                download_id: int,
                completed_at: str
        ) -> None:
    
            query = """
            UPDATE downloads
            SET completed_at = ?
            WHERE id = ?
            """
    
            self.db_manager.execute_query(
                query,
                (
                    completed_at,
                    download_id
                )
            )

    #7
    def update_error(
                self,
                download_id: int,
                error_message: str
        ) -> None:
    
            query = """
            UPDATE downloads
            SET 
                status = ?,
                error_message = ?
            WHERE id = ?
            """
    
            self.db_manager.execute_query(
                query,
                (
                    "error",
                    error_message,                    
                    download_id
                )
            )

    #8
    def update_file_info(
            self,
            download_id: int,
            file_name: str | None = None,
            title:str | None = None,
            total_size: int | None = None,
            destination_path:str | None = None
    ) -> None:

        query = """
        UPDATE downloads
        SET 
            file_name = ?,
            title = ?,
            total_size = ?,
            destination_path = ?
        WHERE id = ?
        """

        self.db_manager.execute_query(
              query,
              (
                    file_name,
                    title,
                    total_size,
                    destination_path,
                    download_id
              )
        )

    #9
    def get_active_downloads(self) -> list[dict]:

        query = """
            SELECT *
            FROM downloads
            WHERE status IN ('queued', 'active', 'paused')
            ORDER BY id ASC
        """

        return self.db_manager.fetch_all(query)