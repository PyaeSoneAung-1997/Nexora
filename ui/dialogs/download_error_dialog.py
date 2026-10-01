# ============================================================
# Nexora - Download Error Dialog
# Version: 1.0.0
# ============================================================

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class DownloadErrorDialog(QDialog):

    def __init__(
        self,
        file_name: str,
        error_message: str,
        parent=None,
    ):
        super().__init__(parent)

        self.file_name = file_name
        self.error_message = error_message

        self.setWindowTitle("Download Error")
        self.setMinimumWidth(450)
        self.setModal(False)

        self._setup_ui()
        self._connect_signals()

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
            "Download Failed"
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
            self.name_label.textInteractionFlags()
            | self.name_label.textInteractionFlags()
        )

        self.main_layout.addWidget(
            self.name_label
        )

        # ----------------------------------------------------
        # Error Message
        # ----------------------------------------------------

        self.error_label = QLabel(
            self.error_message
        )

        self.error_label.setWordWrap(True)

        self.error_label.setStyleSheet("""
            QLabel {
                color: #EF4444;
            }
        """)

        self.main_layout.addWidget(
            self.error_label
        )

        # ----------------------------------------------------
        # Button
        # ----------------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.close_button = QPushButton(
            "Close"
        )

        button_layout.addWidget(
            self.close_button
        )

        self.main_layout.addLayout(
            button_layout
        )

    # ========================================================
    # Connect Signals
    # ========================================================

    def _connect_signals(self):

        self.close_button.clicked.connect(
            self.accept
        )
