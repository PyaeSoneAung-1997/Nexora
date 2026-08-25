from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QApplication
)

# import sys
class SchduleDialog(QDialog):

    
    # url_submitted = pyqtSignal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Add URL")
        self.resize(500, 150)

        layout = QVBoxLayout(self)

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Enter URL..."
        )

# app = QApplication(sys.argv)

# app.psetWindowTitle("Nexora")
# app.resize(1000, 700)
# app.show()

# sys.exit(app.exec())