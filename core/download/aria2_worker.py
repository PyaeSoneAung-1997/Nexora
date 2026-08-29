import time

from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)


class Aria2DownloadWorker(QObject):

    progress = pyqtSignal(dict)
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

                speed = int(
                    status.get(
                        "downloadSpeed",
                        0
                    )
                )

                if total > 0:
                    percent = int(
                        completed * 100 / total
                    )

                else:
                    percent = 0
                

                self.progress.emit(
                    {
                        "status":state,
                        "completed":completed,
                        "total":total,
                        "speed":speed,
                        "percent":percent
                    }
                )

                print(
                    "Aria2:",state,completed,"/",total,"Speed:",speed
                )
                # -------------------------
                # Completed
                # -------------------------

                if state == "complete":

                    self.progress.emit(
                        {
                        "status":"complete",
                        "completed":completed,
                        "total": total,
                        "speed":0,
                        "percent":100
                        }
                    )

                    self.finished.emit(
                        True
                    )

                    return

                # -------------------------
                # Failed
                # 
                # -------------------------

                if state == "error":

                    self.finished.emit(
                        False
                    )

                    return

                # -------------------------
                # Wait
                # -------------------------
                if state == "removed":
                    self.finished.emit(
                        False
                    )
                    return
                time.sleep(0.5)

        except Exception as e:

            print(
                "Aria2 worker error:",
                e
            )

            self.finished.emit(
                False
            )