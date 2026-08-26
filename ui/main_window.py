import sys

from PyQt6.QtWidgets import (
    # QApplication,
    QMainWindow,
    QMessageBox,
    # QToolBar,
    # QDialog, 
    # QLineEdit, 
    # QPushButton,
    # QVBoxLayout
)
from PyQt6.QtGui import QIcon
# from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow

from ui.components.toolbar import toolbar
from ui.components.menubar import menubar

from ui.dialogs.add_url_dialog import AddUrlDialog

from core.url.url_manager import URLManager

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nexora")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("Nexora_logo.ico"))

        self.menu_bar = menubar(self)

        self.setMenuBar(self.menu_bar) 

        self.tool_bar = toolbar(self)   

        self.addToolBar(self.tool_bar)
        #Add url dialog
        self.tool_bar.add_url_action.triggered.connect(
            self.open_add_url_dialog
        )
        self.tool_bar.schdule_action.triggered.connect(
            self.open_schdule_dialog
        )

        self.url_manager = URLManager()

    #Menubar
    def new_file(self):
        print("Click New File")

    #Toolbar  
    def open_add_url_dialog(self):

        dialog = AddUrlDialog(self)
        dialog.url_submitted.connect(
            self.handle_url
        )

        dialog.exec()

    #Toolbar
    def handle_url(self,url):
        url_check = self.url_manager.analyze(url)

        if not url_check["valid"]:
            QMessageBox.warning(
                self,
                "Invalid URL",
                url_check["error"]
            )
            self.open_add_url_dialog()
            return 

        print(url_check) 
        
    
    #Schdule
    def open_schdule_dialog(self):
        print("Oki Schdule")
        # dialog = SchduleDialog(self)
        
        

#     def open_file(self):
#         print("Open ကို နှိပ်လိုက်ပြီ")

#     def show_about(self):

#         QMessageBox.information(
#                     self,
#                     "About Nexora",
#                     "Nexora Download Manager\nVersion 1.0"
#                 )

#     def add_download(self):
#         dialog = AddUrlDialog(self)

#         dialog.url_submitted.connect(self.handle_url)
#         dialog.exec()
                
#     def resume_download(self):
#         print("Resume ကို နှိပ်လိုက်ပြီ")

#     def pause_download(self):
#         print("Pause ကို နှိပ်လိုက်ပြီ")

#     def stop_download(self):
#         print("Stop ကို နှိပ်လိုက်ပြီ")

#     def stop_all_download(self):
#             print("Stop All ကို နှိပ်လိုက်ပြီ")    

#     def delete_download(self):
#         print("delete ကို နှိပ်လိုက်ပြီ")

#     def options_download(self):
#         print("Options ကို နှိပ်လိုက်ပြီ")

#     def schdule_download(self):
#         print("schdule ကို နှိပ်လိုက်ပြီ")

#     def handle_url(self, url):
#         print("Logic ဆီပို့မယ့် URL:", url)
        
# class AddUrlDialog(QDialog):

#     url_submitted = pyqtSignal(str)

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.setWindowTitle("Add URL")
#         self.resize(500, 150)

#         self.setup_ui()

#     def setup_ui(self):

#         layout = QVBoxLayout()

#         self.url_input = QLineEdit()
#         self.url_input.setPlaceholderText("Enter URL...")

#         self.go_button = QPushButton("Go")

#         layout.addWidget(self.url_input)
#         layout.addWidget(self.go_button)

#         self.setLayout(layout)

#         self.go_button.clicked.connect(self.go)
        
#     def go(self):

#         url = self.url_input.text().strip()

#         if not url:
#             return
        
#         self.url_submitted.emit(url)        
#         self.accept()


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# sys.exit(app.exec())