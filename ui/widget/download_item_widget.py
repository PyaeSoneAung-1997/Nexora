from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QProgressBar,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)

from PyQt6.QtCore import pyqtSignal


class DownloadItemWidget(QWidget):

    pause_clicked = pyqtSignal()
    resume_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()

    def __init__(self, download_id, file_name, parent=None):

        super().__init__(parent)

        self.download_id = download_id

        self.file_name_label = QLabel(file_name)

        self.status_label = QLabel("Queued")

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange( 0, 100 )

        self.progress_bar.setValue( 0 )

        self.pause_button = QPushButton( "Pause" )

        self.resume_button = QPushButton( "Resume" )

        self.stop_button = QPushButton( "Stop" )
        
        self.pause_button.clicked.connect(
            self.pause_clicked.emit
        )

        self.resume_button.clicked.connect(
            self.resume_clicked.emit
        )

        self.stop_button.clicked.connect(
            self.stop_clicked.emit
        )

        info_layout = QVBoxLayout()

        info_layout.addWidget(
            self.file_name_label
        )

        info_layout.addWidget(
            self.status_label
        )

        info_layout.addWidget(
            self.progress_bar
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.pause_button
        )

        button_layout.addWidget(
            self.resume_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        main_layout = QVBoxLayout(
            self
        )

        main_layout.addLayout(
            info_layout
        )

        main_layout.addLayout(
            button_layout
        )

    def set_progress(self, progress):

        self.progress_bar.setValue(
            progress
        )

        self.status_label.setText(
            f"Downloading... {progress}%"
        )

    def set_completed(self):

        self.progress_bar.setValue(
            100
        )

        self.status_label.setText(
            "Completed"
        )


    def set_failed(self, error):

        self.status_label.setText(
            f"Failed: {error}"
        )

    def set_paused(self):

        self.status_label.setText(
            "Paused"
        )


    def set_resumed(self):

        self.status_label.setText(
            "Downloading..."
        )


    def set_stopped(self):

        self.status_label.setText(
            "Stopped"
        )