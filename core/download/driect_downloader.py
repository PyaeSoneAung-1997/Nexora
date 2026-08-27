import requests
import os


class DirectDownloader:

    def __init__(self, db_manager):

        self.db = db_manager

    def download(
        self,
        download_id,
        progress_callback=None,
        pause_event=None,
        stop_event=None
    ):

        # --------------------------------
        # DB ထဲက Download information ယူ
        # --------------------------------

        download = self.db.fetch_one(
            """
            SELECT *
            FROM downloads
            WHERE id = ?
            """,
            (download_id,)
        )

        if not download:

            print(
                "Download item not found"
            )

            return False

        url = download["url"]

        print(
            "Start Downloading:",
            url
        )

        try:

            response = requests.get(
                url,
                stream=True,
                timeout=30
            )

            response.raise_for_status()

            total_size = int(
                response.headers.get(
                    "Content-Length",
                    0
                )
            )

            print(
                "Total size:",
                total_size
            )

            # --------------------------------
            # File Name
            # --------------------------------

            file_name = url.split("/")[-1]

            if not file_name:

                file_name = (
                    "downloaded_file"
                )

            download_folder = "downloads"

            os.makedirs(
                download_folder,
                exist_ok=True
            )

            file_path = os.path.join(
                download_folder,
                file_name
            )

            # --------------------------------
            # DB → Downloading
            # --------------------------------

            self.db.execute_query(
                """
                UPDATE downloads
                SET file_name = ?,
                    destination_path = ?,
                    total_size = ?,
                    status = 'downloading',
                    started_at = datetime(
                        'now',
                        'localtime'
                    )
                WHERE id = ?
                """,
                (
                    file_name,
                    file_path,
                    total_size,
                    download_id
                )
            )

            downloaded = 0

            # --------------------------------
            # Download
            # --------------------------------

            with open(
                file_path,
                "wb"
            ) as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 64
                ):

                    if not chunk:
                        continue

                    # ========================
                    # STOP
                    # ========================

                    if (
                        stop_event
                        and stop_event.is_set()
                    ):

                        print(
                            "Download stopped"
                        )

                        self.db.execute_query(
                            """
                            UPDATE downloads
                            SET status = 'stopped'
                            WHERE id = ?
                            """,
                            (download_id,)
                        )

                        return False

                    # ========================
                    # PAUSE
                    # ========================

                    if pause_event:

                        pause_event.wait()

                    # ========================
                    # Write
                    # ========================

                    file.write(
                        chunk
                    )

                    downloaded += len(
                        chunk
                    )

                    # ========================
                    # DB Progress
                    # ========================

                    self.db.execute_query(
                        """
                        UPDATE downloads
                        SET downloaded_bytes = ?,
                            progress = ?
                        WHERE id = ?
                        """,
                        (
                            downloaded,
                            int(
                                downloaded * 100
                                / total_size
                            )
                            if total_size > 0
                            else 0,
                            download_id
                        )
                    )

                    # ========================
                    # UI Progress
                    # ========================

                    if (
                        progress_callback
                        and total_size > 0
                    ):

                        progress = int(
                            downloaded * 100
                            / total_size
                        )

                        progress_callback(
                            progress
                        )

            # --------------------------------
            # Completed
            # --------------------------------

            self.db.execute_query(
                """
                UPDATE downloads
                SET downloaded_bytes = ?,
                    progress = 100,
                    status = 'completed',
                    completed_at = datetime(
                        'now',
                        'localtime'
                    )
                WHERE id = ?
                """,
                (
                    downloaded,
                    download_id
                )
            )

            print(
                "Download completed"
            )

            print(
                "File:",
                file_path
            )

            return True

        except Exception as e:

            print(
                "Download failed:",
                e
            )

            self.db.execute_query(
                """
                UPDATE downloads
                SET status = 'failed',
                    error_message = ?
                WHERE id = ?
                """,
                (
                    str(e),
                    download_id
                )
            )

            return False