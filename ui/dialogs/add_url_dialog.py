from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel
)


class AddUrlDialog(QDialog):

    # URL ကို MainWindow ဆီပို့မယ့် Signal
    url_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        
        super().__init__(parent)

        self.setWindowTitle("Add URL")
        self.setFixedSize(600, 100)

        layout = QVBoxLayout(self)        
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)

        self.label = QLabel("Add URL Address:")
        self.label.setFixedWidth(100)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL...")

        self.go_button = QPushButton("Go")

        url_layout.addWidget(self.label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.go_button)

        layout.addLayout(url_layout)

                
        # Go → go()
        self.go_button.clicked.connect(
            self.go
        )

    def go(self):

        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(
                self,
                "Input Error", 
                "Please enter a valid URL!" 
            )
            return
        
        # URL ကို MainWindow ဆီပို့
        self.url_submitted.emit(url)

        # Dialog ပိတ်
        self.accept()

    
            