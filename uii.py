import sys

from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QToolBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

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

        toolbar.setIconSize(QSize(75, 75))
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        self.add_action = toolbar.addAction(
            QIcon("icons/add.ico"),
            "Add"
        )

        self.start_action = toolbar.addAction(
            QIcon("icons/start.ico"),
            "Start"
        )

        self.stop_action = toolbar.addAction(
            QIcon("icons/stop.ico"),
            "Stop"
        )

        self.pause_action = toolbar.addAction(
            QIcon("icons/pause.ico"),
            "Pause"
        )

    # =========================
    # Signal
    # =========================
    def connect_signals(self):

        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self.show_about)

        self.add_action.triggered.connect(self.add_download)
        self.start_action.triggered.connect(self.start_download)
        self.stop_action.triggered.connect(self.stop_download)
        self.pause_action.triggered.connect(self.pause_download)

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
        print("Add ကို နှိပ်လိုက်ပြီ")

    def start_download(self):
        print("Start ကို နှိပ်လိုက်ပြီ")

    def stop_download(self):
        print("Stop ကို နှိပ်လိုက်ပြီ")

    def pause_download(self):
        print("Pause ကို နှိပ်လိုက်ပြီ")

        



app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())