# ============================================================
# Nexora - Download Complete Dialog
# Version: 1.0.0
# ============================================================

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class DownloadCompleteDialog(QDialog):

    # Signals
    open_file_requested = pyqtSignal()
    open_folder_requested = pyqtSignal()

    def __init__(
        self,
        file_name: str,
        file_size: str,
        file_path: str,
        parent=None,
    ):
        super().__init__(parent)

        self.file_name = file_name
        self.file_size = file_size
        self.file_path = file_path

        self.setWindowTitle("Download Completed")
        self.setMinimumWidth(450)
        self.setModal(False)

        self._setup_ui()
        # self._connect_signals()

    # ========================================================
    # UI Setup
    # ========================================================

    def _setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(
            20, 20, 20, 20
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.title_label = QLabel(
            "Download Completed"
        )

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(
            self.title_label
        )

        # ----------------------------------------------------
        # File Name
        # ----------------------------------------------------

        self.name_label = QLabel(
            self.file_name
        )

        self.name_label.setWordWrap(True)

        self.name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.main_layout.addWidget(
            self.name_label
        )

        # ----------------------------------------------------
        # File Size
        # ----------------------------------------------------

        self.size_label = QLabel(
            f"Size: {self.file_size}"
        )

        self.main_layout.addWidget(
            self.size_label
        )

        # ----------------------------------------------------
        # File Path
        # ----------------------------------------------------

        self.path_label = QLabel(
            f"Location: {self.file_path}"
        )

        self.path_label.setWordWrap(True)

        self.path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.main_layout.addWidget(
            self.path_label
        )

        # ----------------------------------------------------
        # Buttons
