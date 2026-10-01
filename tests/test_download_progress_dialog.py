
# ============================================================
# Nexora - Download Progress Dialog Test
# ============================================================

import sys

from PyQt6.QtWidgets import QApplication

from ui.dialogs.download_progress_dialog import (
    DownloadProgressDialog,
)


def main():
    app = QApplication(sys.argv)

    dialog = DownloadProgressDialog(
        file_name="example_video.mp4"
    )

    # --------------------------------------------------------
    # Initial Progress
    # --------------------------------------------------------

    dialog.update_progress(
        progress=67,
        downloaded_bytes=670 * 1024 * 1024,
        total_bytes=1024 * 1024 * 1024,
        speed=5 * 1024 * 1024,
        time_left="1 min 05 sec",
        connections=4,
        status="downloading",
    )

    # --------------------------------------------------------
    # Connect Test Signals
    # --------------------------------------------------------

    def on_pause():
        print("Pause requested")

        dialog.update_progress(
            progress=67,
            downloaded_bytes=670 * 1024 * 1024,
            total_bytes=1024 * 1024 * 1024,
            speed=0,
            time_left="Paused",
            connections=0,
            status="paused",
        )

    def on_resume():
        print("Resume requested")

        dialog.update_progress(
            progress=67,
            downloaded_bytes=670 * 1024 * 1024,
            total_bytes=1024 * 1024 * 1024,
            speed=5 * 1024 * 1024,
            time_left="1 min 05 sec",
            connections=4,
            status="downloading",
        )

    def on_cancel():
        print("Cancel requested")

        dialog.update_progress(
            progress=67,
            downloaded_bytes=670 * 1024 * 1024,
            total_bytes=1024 * 1024 * 1024,
            speed=0,
            time_left="Cancelled",
            connections=0,
            status="cancelled",
        )

    dialog.pause_requested.connect(on_pause)
    dialog.resume_requested.connect(on_resume)
    dialog.cancel_requested.connect(on_cancel)

    # --------------------------------------------------------
    # Show Dialog
    # --------------------------------------------------------

    dialog.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()