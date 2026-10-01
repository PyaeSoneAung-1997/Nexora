from core.database.db_manager import DatabaseManager

class BaseRepository:
    def __init__(
            self,
            db_manager: DatabaseManager,
            table_name:str
            ):
        self.db_manager = db_manager
        self.table_name = table_name

    
    def get_by_id(
            self, 
            record_id: int
            ) -> dict | None:
        query = f"""
        SELECT * 
        FROM {self.table_name} 
        WHERE id = ?
        """
        return  self.db_manager.fetch_one(query, (record_id,))

    def get_all(
            self
            ) -> list[dict]:
        query = f"""
        SELECT * 
        FROM {self.table_name}
        """
        return self.db_manager.fetch_all(query)

    def delete(
            self,
            record_id: int
            ) -> None:
        query = f"""
        DELETE FROM {self.table_name}
        WHERE id = ?
        """
        self.db_manager.execute_query(query, (record_id,))