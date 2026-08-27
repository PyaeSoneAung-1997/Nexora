from PyQt6.QtCore import QObject, pyqtSignal


class DownloadWorker(QObject):

    finished = pyqtSignal(bool)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, downloader, download_id):

        super().__init__()

        self.downloader = downloader
        self.download_id = download_id

        self.pause_event = None
        self.stop_event = None

    def set_events(
        self,
        pause_event,
        stop_event
    ):

        self.pause_event = pause_event
        self.stop_event = stop_event

    def run(self):

        try:

            success = self.downloader.download(
                self.download_id,
                self.progress.emit,
                self.pause_event,
                self.stop_event
            )

            self.finished.emit(success)

        except Exception as e:

            self.error.emit(str(e))
            self.finished.emit(False)