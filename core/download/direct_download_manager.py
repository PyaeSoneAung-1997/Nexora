from core.database.db_manager import DatabaseManager

class DirectManager:

    def __init__(self, db_manager):

        self.db = DatabaseManager()

    def add_url(self, url):

        query = """
        INSERT INTO downloads (
            url,
            url_type,
            status
        )
        VALUES (?, ?, ?)
        """

        return self.db.execute_query(
            query,
            (url, "direct", "queued")
        )