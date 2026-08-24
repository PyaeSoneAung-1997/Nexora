import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QDialog,
    QLineEdit,
    QLabel,
    QMessageBox
)


# =====================================
# URL Manager
# =====================================

class URLManager:

    def process(self, url):

        url = url.strip()

        if not url:
            return {
                "valid": False,
                "message": "Empty URL"
            }

        if "drive.google.com" in url:
            return {
                "valid": True,
                "type": "google_drive",
                "url": url
            }

        return {
            "valid": True,
            "type": "direct_link",
            "url": url
        }


# =====================================
# Add URL Dialog
# =====================================

class AddURLDialog(QDialog):

    url_processed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add URL")
        self.resize(500, 120)

        layout = QVBoxLayout()

        self.label = QLabel(
            "Enter URL:"
        )

        self.url_edit = QLineEdit()

        self.url_edit.setPlaceholderText(
            "https://..."
        )

        self.btn_add = QPushButton(
            "Add"
        )

        layout.addWidget(self.label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.btn_add)

        self.setLayout(layout)

        self.btn_add.clicked.connect(
            self.process_url
        )

    def process_url(self):

        url = self.url_edit.text()

        result = URLManager().process(url)

        if not result["valid"]:
            QMessageBox.warning(
                self,
                "Error",
                result["message"]
            )
            return

        self.url_processed.emit(result)

        self.accept()


# =====================================
# Main Window
# =====================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nexora Demo")
        self.resize(800, 500)

        self.queue = []

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        self.btn_add_url = QPushButton(
            "Add URL"
        )

        self.url_list = QListWidget()

        layout.addWidget(self.btn_add_url)
        layout.addWidget(self.url_list)

        central.setLayout(layout)

        self.btn_add_url.clicked.connect(
            self.open_add_url_dialog
        )

    def open_add_url_dialog(self):

        dialog = AddURLDialog()

        dialog.url_processed.connect(
            self.handle_url_result
        )

        dialog.exec()

    def handle_url_result(self, result):

        self.queue.append(result)

        item_text = (
            f'Type: {result["type"]} | '
            f'URL: {result["url"]}'
        )

        self.url_list.addItem(item_text)

        print("\n========== QUEUE ==========")

        for item in self.queue:
            print(item)

        print("===========================\n")

        # Route Example

        if result["type"] == "google_drive":
            print("→ Send To Drive Scanner")

        elif result["type"] == "direct_link":
            print("→ Send To Download Queue")


# =====================================
# Application Start
# =====================================

def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()