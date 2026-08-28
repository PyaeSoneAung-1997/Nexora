import time

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)


class Aria2DownloadWorker(QObject):

    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, aria2_engine, gid):

        super().__init__()

        self.aria2 = aria2_engine
        self.gid = gid

        self.running = True

    def run(self):

        try:

            while self.running:

                status = self.aria2.get_status(
                    self.gid
                )

                state = status.get(
                    "status"
                )

                completed = int(
                    status.get(
                        "completedLength",
                        0
                    )
                )

                total = int(
                    status.get(
                        "totalLength",
                        0
                    )
                )

                # -------------------------
                # Progress
                # -------------------------

                if total > 0:

                    progress = int(
                        completed * 100 / total
                    )

                    self.progress.emit(
                        progress
                    )

                print(
                    "Aria2:",
                    state,
                    completed,
                    "/",
                    total
                )

                # -------------------------
                # Completed
                # -------------------------

                if state == "complete":

                    self.progress.emit(
                        100
                    )

                    self.finished.emit(
                        True
                    )

                    return

                # -------------------------
                # Failed
                # -------------------------

                if state == "error":

                    self.finished.emit(
                        False
                    )

                    return

                # -------------------------
                # Wait
                # -------------------------

                time.sleep(0.5)

        except Exception as e:

            print(
                "Aria2 worker error:",
                e
            )

            self.finished.emit(
                False
            )