from datetime import timezone,datetime

from core.database.db_manager import DatabaseManager

class AccountRepository:
    def __init__(self,  db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, 
               email:str, 
               name:str | None, 
               token_path:str,
               status:str = "pending") -> int:

        created_at = datetime.now(timezone.utc).isoformat()
        last_used_at = datetime.now(timezone.utc).isoformat()
        
        query = """
        INSERT INTO accounts (
            email, 
            name, 
            token_path, 
            status,
            created_at,
            last_used_at
        )
        VALUES (?, ?, ?, ?, ?,?)
        """
        return self.db_manager.execute_query(
            query, (
                email, 
                name, 
                token_path, 
                status,
                created_at,
                last_used_at,
            )
        )

    def get_by_email(self, email: str) -> dict | None:
        query = """
        SELECT * FROM accounts WHERE email = ?
        """
        return self.db_manager.fetch_one(query, (email,))

    def update_status(self, account_id: int, status: str) -> None:
        query = """
        UPDATE accounts SET status = ? WHERE id = ?
        """
        self.db_manager.execute_query(query, (status, account_id))

    def update_last_used(self, account_id: int) -> None:
        query = """
        UPDATE accounts SET last_used_at = datetime('now')
        WHERE id = ?
        """
        self.db_manager.execute_query(query, (account_id,))