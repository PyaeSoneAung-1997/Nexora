from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)


class AddUrlDialog(QDialog):

    # URL ကို MainWindow ဆီပို့မယ့် Signal
    url_submitted = pyqtSignal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Add URL")
        self.resize(500, 150)

        layout = QVBoxLayout(self)

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Enter URL..."
        )

        self.go_button = QPushButton("Go")

        layout.addWidget(self.url_input)
        layout.addWidget(self.go_button)

        # Go → go()
        self.go_button.clicked.connect(
            self.go
        )

    def go(self):

        url = self.url_input.text().strip()

        if not url:
            return

        # URL ကို MainWindow ဆီပို့
        self.url_submitted.emit(url)

        # Dialog ပိတ်
        self.accept()