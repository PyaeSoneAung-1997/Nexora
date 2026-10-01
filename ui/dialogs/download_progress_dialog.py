
# ============================================================
# Nexora - Download Progress Dialog
# Version: 1.0.0
# ============================================================

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QGridLayout,
    QMessageBox,
)


class DownloadProgressDialog(QDialog):

    # Signals
    pause_requested = pyqtSignal()
    resume_requested = pyqtSignal()
    cancel_requested = pyqtSignal()

    def __init__(
        self,
        file_name: str,
        parent=None,
    ):
        super().__init__(parent)

        self.file_name = file_name
        self.is_paused = False
        self.is_finished = False

        self.setWindowTitle("Download Progress")
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
        # File Name
        # ----------------------------------------------------

        self.name_label = QLabel(self.file_name)
        self.name_label.setWordWrap(True)
        self.name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.name_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(self.name_label)

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.status_label = QLabel("Queued")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #3B82F6;
                font-size: 12px;
            }
        """)

        self.main_layout.addWidget(self.status_label)

        # ----------------------------------------------------
        # Progress Bar
        # ----------------------------------------------------

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setTextVisible(True)

        self.main_layout.addWidget(self.progress_bar)

        # ----------------------------------------------------
        # Downloaded Size
        # ----------------------------------------------------

        self.size_label = QLabel("0 B / Unknown")
        self.size_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        self.main_layout.addWidget(self.size_label)

        # ----------------------------------------------------
        # Download Information
        # ----------------------------------------------------

        info_layout = QGridLayout()
        info_layout.setHorizontalSpacing(30)
        info_layout.setVerticalSpacing(12)

        self.speed_value = QLabel("0 B/s")
        self.time_value = QLabel("--")
        self.connections_value = QLabel("0")
        self.status_value = QLabel("Queued")

        info_layout.addWidget(
            QLabel("Speed"),
            0, 0
        )
        info_layout.addWidget(
            self.speed_value,
            0, 1
        )

        info_layout.addWidget(
            QLabel("Time Left"),
            1, 0
        )
        info_layout.addWidget(
            self.time_value,
            1, 1
        )

        info_layout.addWidget(
            QLabel("Connections"),
            2, 0
        )
        info_layout.addWidget(
            self.connections_value,
            2, 1
        )

        info_layout.addWidget(
            QLabel("Status"),
            3, 0
        )
        info_layout.addWidget(
            self.status_value,
            3, 1
        )

        self.main_layout.addLayout(info_layout)

        # ----------------------------------------------------
        # Error Message
        # ----------------------------------------------------

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("""
            QLabel {
                color: #EF4444;
            }
        """)

        self.error_label.hide()
        self.main_layout.addWidget(self.error_label)

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.pause_button = QPushButton("Pause")
        self.resume_button = QPushButton("Resume")
        self.cancel_button = QPushButton("Cancel")

        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(True)

        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.resume_button)
        button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(button_layout)

    # ========================================================
    # Connect Signals
    # ========================================================

    def _connect_signals(self):
        self.pause_button.clicked.connect(
            self._on_pause_clicked
        )

        self.resume_button.clicked.connect(
            self._on_resume_clicked
        )

        self.cancel_button.clicked.connect(
            self._on_cancel_clicked
        )

    # ========================================================
    # Pause / Resume / Cancel
    # ========================================================

    def _on_pause_clicked(self):
        if self.is_finished or self.is_paused:
            return

        self.pause_requested.emit()

    def _on_resume_clicked(self):
        if self.is_finished or not self.is_paused:
            return

        self.resume_requested.emit()

    def _on_cancel_clicked(self):
        if self.is_finished:
            self.close()
            return

        answer = QMessageBox.question(
            self,
            "Cancel Download",
            "Are you sure you want to cancel this download?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.cancel_requested.emit()

    # ========================================================
    # Update Progress
    # ========================================================

    def update_progress(
        self,
        progress: int,
        downloaded_bytes: int,
        total_bytes: int,
        speed: int,
        time_left: str,
        connections: int,
        status: str,
    ):
        """
        Download အခြေအနေကို UI ပေါ်မှာ update လုပ်သည်။
        """

        progress = max(0, min(100, progress))

        self.progress_bar.setValue(progress)

        self.size_label.setText(
            f"{self._format_size(downloaded_bytes)} / "
            f"{self._format_size(total_bytes)}"
        )

        self.speed_value.setText(
            f"{self._format_size(speed)}/s"
        )

        self.time_value.setText(time_left)

        self.connections_value.setText(
            str(connections)
        )

        self.status_label.setText(status.capitalize())
        self.status_value.setText(status.capitalize())

        self._update_button_states(status)

    # ========================================================
    # Update Status
    # ========================================================

    def _update_button_states(self, status: str):
        status = status.lower()

        self.is_paused = status == "paused"

        self.is_finished = status in {
            "completed",
            "failed",
            "cancelled",
        }

        self.pause_button.setEnabled(
            status == "active"
        )

        self.resume_button.setEnabled(
            status == "paused"
        )

        if self.is_finished:
            self.cancel_button.setText("Close")

        if status == "finished":
            self.progress_bar.setValue(100)

    # ========================================================
    # Error
    # ========================================================

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()

    # ========================================================
    # Format File Size
    # ========================================================

    @staticmethod
    def _format_size(size: int) -> str:
        if size < 0:
            size = 0

        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(size)

        for unit in units:
            if value < 1024 or unit == "TB":
                if unit == "B":
                    return f"{int(value)} {unit}"

                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} TB"