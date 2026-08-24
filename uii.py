import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QToolBar,
    QDialog, 
    QLineEdit, 
    QPushButton,
    QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtCore import pyqtSignal

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.connect_signals()

    def setup_window(self):
        self.setWindowTitle("Nexora")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("Nexora_logo.ico"))

    def setup_menu_bar(self):

        menu_bar = self.menuBar()
        #File
        file_menu = menu_bar.addMenu("File")

        self.new_action = file_menu.addAction("New")
        self.open_action = file_menu.addAction("Open")
        file_menu.addSeparator()
        self.exit_action = file_menu.addAction("Exit")

         # Edit
        edit_menu = menu_bar.addMenu("Edit")

        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # View
        view_menu = menu_bar.addMenu("View")

        view_menu.addAction("Sidebar")
        view_menu.addAction("Toolbar")

        # Help
        help_menu = menu_bar.addMenu("Help")
        
        self.about_action = help_menu.addAction("About")

    # =========================
    # Toolbar
    # =========================
    def setup_toolbar(self):

        toolbar = QToolBar("Main Toolbar", self)

        toolbar.setIconSize(QSize(32, 32))
        toolbar.setMovable(False)

        toolbar.setToolButtonStyle(
        Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        self.addToolBar(toolbar)

        self.add_action = toolbar.addAction(
            QIcon("icon/add_url.png"),
            "Add"
        )

        self.resume_action = toolbar.addAction(
            QIcon("icon/resume.png"),
            "Resume"
        )

        self.pause_action = toolbar.addAction(
            QIcon("icon/pause.png"),
            "Pause"
        )
        
        self.stop_action = toolbar.addAction(
            QIcon("icon/stop.png"),
            "Stop"
        )

        self.stop_all_action = toolbar.addAction(
            QIcon("icon/stop_all.png"),
            "Stop All"
        )  

        self.delete_action = toolbar.addAction(
            QIcon("icon/delete.png"),
            "Delete"
        )

        self.options_action = toolbar.addAction(
            QIcon("icon/options.png"),
            "Options"
        )

        self.schdule_action = toolbar.addAction(
            QIcon("icon/schdule.png"),
            "Schdule"
        )

        for action in [
        self.add_action,
        self.resume_action,
        self.pause_action,
        self.stop_action,
        self.stop_all_action,
        self.delete_action,
        self.options_action,
        self.schdule_action
        ]:
            button = toolbar.widgetForAction(action)

            if button:
                button.setFixedSize(70, 70)

    # =========================
    # Signal
    # =========================
    def connect_signals(self):

        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self.show_about)

        self.add_action.triggered.connect(self.add_download)
        self.resume_action.triggered.connect(self.resume_download)
        self.pause_action.triggered.connect(self.pause_download)
        self.stop_action.triggered.connect(self.stop_download)
        self.stop_all_action.triggered.connect(self.stop_all_download)        
        self.delete_action.triggered.connect(self.delete_download)
        self.options_action.triggered.connect(self.options_download)
        self.schdule_action.triggered.connect(self.schdule_download)        
        

    # =========================
    # Logic Test
    # =========================
    def new_file(self):
        print("New ကို နှိပ်လိုက်ပြီ")

    def open_file(self):
        print("Open ကို နှိပ်လိုက်ပြီ")

    def show_about(self):

        QMessageBox.information(
                    self,
                    "About Nexora",
                    "Nexora Download Manager\nVersion 1.0"
                )

    def add_download(self):
        dialog = AddUrlDialog(self)

        dialog.url_submitted.connect(self.handle_url)
        dialog.exec()
                
    def resume_download(self):
        print("Resume ကို နှိပ်လိုက်ပြီ")

    def pause_download(self):
        print("Pause ကို နှိပ်လိုက်ပြီ")

    def stop_download(self):
        print("Stop ကို နှိပ်လိုက်ပြီ")

    def stop_all_download(self):
            print("Stop All ကို နှိပ်လိုက်ပြီ")    

    def delete_download(self):
        print("delete ကို နှိပ်လိုက်ပြီ")

    def options_download(self):
        print("Options ကို နှိပ်လိုက်ပြီ")

    def schdule_download(self):
        print("schdule ကို နှိပ်လိုက်ပြီ")

    # def handle_url(self, url):
    #     print("Logic ဆီပို့မယ့် URL:", url)
        
class AddUrlDialog(QDialog):

    url_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add URL")
        self.resize(500, 150)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL...")

        self.go_button = QPushButton("Go")

        layout.addWidget(self.url_input)
        layout.addWidget(self.go_button)

        self.setLayout(layout)

        self.go_button.clicked.connect(self.go)
        
    def go(self):

        url = self.url_input.text().strip()

        if not url:
            return
        
        self.url_submitted.emit(url)        
        self.accept()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())