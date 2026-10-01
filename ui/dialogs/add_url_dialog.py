from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)


class AddURLDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New URL")
        self.setFixedSize(600, 100)

        # Main Layout
        layout = QVBoxLayout(self)

        # URL
        url_label = QLabel("URL Address:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL...")

        layout.addWidget(url_label)
        layout.addWidget(self.url_input)

        # Buttons
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.add_button    = QPushButton("Add")

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # Connections
        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)