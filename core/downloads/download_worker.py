from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class DownloadWorker(QObject):

    progress_changed = pyqtSignal(dict)
    download_completed = pyqtSignal(dict)
    download_error = pyqtSignal(dict)

    finished = pyqtSignal()

    def __init__(
        self,
        aria2_engine,
        gid: str,
        download_id: int
    ):
        super().__init__()

        self.aria2_engine = aria2_engine
        self.gid = gid
        self.download_id = download_id

        self.timer = None

    def start(self):
        self.timer = QTimer(self)

        
        self.timer.timeout.connect(
            self.check_status
        )

        self.timer.start(1000)
        # print("timer")
        # print(self.check_status)

    def stop(self):
        if self.timer is not None:
            self.timer.stop()

    def check_status(self):

        try:
            status = self.aria2_engine.get_status(
                self.gid
            )
            # print("Hi Status")
            # print(status)

            if not status:
                return
            
            print(status)
            self.handle_status(status)

        except Exception as e:

            self.download_error.emit({
                "download_id":self.download_id,
                "gid": self.gid,
                "error": str(e)
            })

            self.stop()

    def handle_status(self, status):

        total_size = int(
            status.get("totalLength", 0)
        )

        downloaded = int(
            status.get("completedLength", 0)
        )

        speed = int(
            status.get("downloadSpeed", 0)
        )

        aria2_status = status.get(
            "status"
        )

        progress = 0

        if total_size > 0:
            progress = int(
                downloaded / total_size * 100
            )
        connections  = int(
            status.get("connections",0)
        )
        data = {
            "gid": self.gid,
            "status": aria2_status,
            "total_size": total_size,
            "downloaded_bytes": downloaded,
            "speed": speed,
            "connections":connections,
            "progress": progress
        }

        if aria2_status == "complete":

            print(aria2_status)

            self.progress_changed.emit(data)

            self.download_completed.emit(data)

            self.stop()

            self.finished.emit()

            return

        if aria2_status == "error":

            self.download_error.emit(data)

            self.stop()

            self.finished.emit()

            return

        self.progress_changed.emit(data)
        # print("progress changed")