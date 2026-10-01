from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal

from config.app_paths import DOWNLOAD_DIR
from ui.components.size_format import SizeFormatter

class DirectDownloadDialog(QDialog):
    
    download_requested = pyqtSignal(dict) 

    def __init__(self, url, info, parent=None):
            super().__init__(parent)
            self.size_formatter = SizeFormatter()
            self.url = url
            self.info = info
            self.setWindowTitle("Direct Download")
            self.setFixedSize(600, 200)

            self.setup_ui()

    def setup_ui(self):
        # print( self.info)
        layout = QVBoxLayout(self)

        url_link = QLabel(f"Download URL: {self.url}")
        layout.addWidget(url_link)

        filename = self.info.get("filename")
        layout.addWidget(QLabel(f"Filename: {filename}"))   

        size = self.size_formatter.format_size(
             self.info.get("size")
             )

        layout.addWidget(QLabel(f"File Size: {size}"))

        # Save To
        save_label = QLabel("Save To:")
        layout.addWidget(save_label)

        save_layout = QHBoxLayout()

        self.save_path_input = QLineEdit()

        self.save_path_input.setText(str(DOWNLOAD_DIR))

        self.browse_button = QPushButton("Browse")

        save_layout.addWidget(self.save_path_input)
        save_layout.addWidget(self.browse_button)

        layout.addLayout(save_layout)

         # Buttons
        button_layout = QHBoxLayout()

        self.download_button = QPushButton("Download")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Signals
        self.browse_button.clicked.connect(
             self.browse_folder
             )
        self.download_button.clicked.connect(
             self.handle_download
             )
        self.cancel_button.clicked.connect(
             self.reject
             )

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if folder:
            self.save_path_input.setText(folder)

    def handle_download(self):
        save_path = self.save_path_input.text().strip()

        if not save_path:
             QMessageBox.warning(
                 self,
                 "Invalid Path",
                 "Please select a valid download path."
             )
             return

        if not Path(save_path).is_dir():
             QMessageBox.warning(
                 self,
                 "Invalid Path",
                 "The selected download path does not exist."
             )
             return

        data = {
            "url": self.url,
            "filename": self.info.get("filename"),
            "size": self.info.get("size"),
            "content_type": self.info.get(
                "content_type"
            ),
            "supports_range": self.info.get(
                "supports_range"
            ),
            "original_url": self.info.get(
                "original_url"
            ),
            "final_url": self.info.get(
                "final_url"
            ),
            "save_path": self.save_path_input.text().strip()
        }

        self.download_requested.emit(data)

