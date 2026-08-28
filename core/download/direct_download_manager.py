from PyQt6.QtCore import QThread
import threading
from core.database.db_manager import DatabaseManager
from core.download.driect_downloader import DirectDownloader
from core.download.download_worker import DownloadWorker
from core.download.aria2_worker import Aria2DownloadWorker

class DirectManager:
     
    def __init__(self, db_manager,aria2_engine):

        self.db = db_manager or DatabaseManager()
        self.aria2 = aria2_engine
        # self.downloader = DirectDownloader(
        #     self.db
        # )
        self.threads = {}
        self.workers = {}
        self.gids = {}
        # self.pause_events = {}
        # self.stop_events = {}


    def add_url(self, url):

        query = """
        INSERT INTO downloads (
            url,
            url_type,
            status
        )
        VALUES (?, ?, ?)
        """

        download_id = self.db.execute_query(
            query,
            (url,"direct","queued")
        )

    #     # print("Download ID:", download_id)

        return download_id

    def start_download(
            self,
            download_id,
            progress_callback=None,
            finished_callback=None
    ):

        if(
            download_id in self.threads
            and self.threads[download_id].isRunning()
        ):
            return

        download = self.db.fetch_one(
            """
            SELECT * 
            FROM downloads
            WHERE id = ?
            """,
            (download_id)
        )

        if not download:
            print(
                "Download not found:",
                download_id
            )

            return

        url = download["url"]

        try:
            gid = self.aria2.addadd_download(
                url,
                "downloads"
            )
        
        except Exception as e:
            print(
                "aria2 start failed:",
                e
            )

            self.db.execute_query(
                """
                UPDATE downloads
                SET status = 'failed',
                    error_message =?
                WHERE id = ?
                """,
                (
                    str(e),
                    download_id
                )
            )

            if finished_callback:
                finished_callback(False)

            return
        print("Download Gid:", gid)

        self.gids[
            download_id
        ] = gid

        self.db.execute_query(
            """
            UPDATE downloads
            SET status = 'downloading'
            WHERE id = ?
            """,
            (download_id,)
        )

        thread = QThread()

        worker = Aria2DownloadWorker(
            self.aria2,
            gid
        )

        worker.moveToThread(
            thread
        )
        

        thread.started.connect(
            worker.run 
        )

        if progress_callback:
            worker.progress.connect(
                progress_callback
            )

        if finished_callback:
            worker.finished.connect(
                finished_callback
            )
    # def start_download(self, download_id, progress_callback=None,
    #                    finished_callback=None):

    #     if (
    #         download_id in self.threads
    #         and self.threads[download_id].isRunning()
    #     ):
    #         return

    #     pause_event = threading.Event()

    #     # Set = Download လုပ်ခွင့်ရှိ
    #     pause_event.set()

    #     stop_event = threading.Event()

    #     self.pause_events[
    #         download_id
    #     ] = pause_event

    #     self.stop_events[
    #         download_id
    #     ] = stop_event

    #     thread = QThread()
    #     worker = DownloadWorker(
    #         self.downloader,
    #         download_id
    #     )

    #     worker.set_events(
    #         pause_event,
    #         stop_event
    #     )

    #     worker.moveToThread(thread)

    #     thread.started.connect(
    #         worker.run
    #     )

    #     if progress_callback:
    #         worker.progress.connect(
    #             progress_callback
    #         )

    #     if finished_callback:
    #         worker.finished.connect(
    #             finished_callback
    #         )
        
    #     worker.finished.connect(
    #         thread.quit
    #     )

    #     worker.finished.connect(
    #         worker.deleteLater
    #     )

    #     thread.finished.connect(
    #         thread.deleteLater
    #     )

    #     self.threads[
    #         download_id
    #     ] = thread

    #     self.workers[
    #         download_id
    #     ] = worker


    #     thread.start()

    # def pause_download(
    #     self,
    #     download_id
    # ):

    #     event = self.pause_events.get(
    #         download_id
    #     )

    #     if event:

    #         event.clear()

    #         print(
    #             "Download Paused:",
    #             download_id
    #         )
    # --------------------------------
    # Resume
    # --------------------------------

    # def resume_download(
    #     self,
    #     download_id
    # ):

    #     event = self.pause_events.get(
    #         download_id
    #     )

    #     if event:

    #         event.set()

    #         print(
    #             "Download Resumed:",
    #             download_id
    #         )

    # --------------------------------
    # Stop
    # --------------------------------

    # def stop_download(
    #     self,
    #     download_id
    # ):

    #     stop_event = self.stop_events.get(
    #         download_id
    #     )

    #     if stop_event:

    #         stop_event.set()

    #         # Pause ဖြစ်နေရင်လည်း
    #         # Worker loop ကနေထွက်နိုင်အောင်
    #         pause_event = self.pause_events.get(
    #             download_id
    #         )

    #         if pause_event:

    #             pause_event.set()

    #         print(
    #             "Download Stopped:",
    #             download_id
    #         )
    def on_progress(self, progress):

        print(
            "Background Progress:",
            progress
        )

    def on_finished(self, success):

        print(
            "Download finished:",
            success
        )