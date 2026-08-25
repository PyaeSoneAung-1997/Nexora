from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QApplication
)

import sys

class SchduleDialog(QDialog):

    
    # url_submitted = pyqtSignal(str

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Schdule")
        self.resize(1000, 500)

        


app = QApplication(sys.argv)

window = SchduleDialog()
window.show()

sys.exit(app.exec())