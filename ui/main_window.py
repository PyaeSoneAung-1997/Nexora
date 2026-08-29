import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout
)
from PyQt6.QtGui import QIcon
# from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow,QWidget

from ui.components.toolbar import toolbar
from ui.components.menubar import menubar

from ui.dialogs.add_url_dialog import AddUrlDialog

from core.url.url_manager import URLManager

# from core.database.db_manager import DatabaseManager
# from core.download.direct_download_manager import DirectManager
# from core.download.driect_downloader import DirectDownloader
# from ui.widget_container import DownloadPage
# from core.download.aria2_engine import Aria2Engine
# from core.download.aria2_worker import Aria2DownloadWorker

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

        # self.url_manager = URLManager()

        # self.db_manager = DatabaseManager()

        # self.aria2_engine = Aria2Engine()
        # self.aria2_engine.start()
        # self.direct_manager = DirectManager(
        #     self.db_manager,
        #     self.aria2_engine
        # )

        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)

        # layout = QVBoxLayout(central_widget)
        # self.download_page = DownloadPage(self)

        # layout.addWidget(
        #     self.download_page
        # )

           
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
    # def handle_pause(self, download_id):

    #     self.direct_manager.pause_download(
    #         download_id
    #     )

    #     widget = self.download_page.download_widgets.get(
    #         download_id
    #     )

    #     if widget:
    #         widget.set_paused()

    # def handle_resume(self, download_id):

    #     self.direct_manager.resume_download(
    #         download_id
    #     )

    #     widget = self.download_page.download_widgets.get(
    #         download_id
    #     )

    #     if widget:
    #         widget.set_resumed()

    # def handle_stop(self, download_id):

    #     self.direct_manager.stop_download(
    #         download_id
    #     )

    #     widget = self.download_page.download_widgets.get(
    #         download_id
    #     )

    #     if widget:
    #         widget.set_stopped()
    #Toolbar
    # def handle_url(self,url):
    #     url_check = self.url_manager.analyze(url)

    #     if not url_check["valid"]:
    #         QMessageBox.warning(
    #             self,
    #             "Invalid URL",
    #             url_check["error"]
    #         )
    #         self.open_add_url_dialog()
    #         return 

    #     # print(url_check) 
        
    #     if url_check["type"] == "direct_file":
    #         download_id = self.direct_manager.add_url(
    #             url_check["url"]
    #         )

    #         # print("Direct URL added:", download_id)
    #         widget = self.download_page.add_download(
    #             download_id,
    #             "Downloading...."
    #         )
    #         # print(widget)

    #         widget.pause_clicked.connect(
    #             lambda checked=False:
    #              self.handle_pause(
    #                 download_id
    #             )
    #         )


    #         widget.resume_clicked.connect(
    #             lambda checked=False:
    #                 self.handle_resume(
    #                     download_id
    #                 )
    #         )

    #         widget.stop_clicked.connect(
    #             lambda checked=False:
    #                 self.handle_stop(
    #                     download_id
    #                 )
    #         )

    #         self.direct_manager.start_download(
    #             download_id,

    #             lambda data:                    
    #                 self.download_page.update_progress(
    #                     download_id,
    #                     data
    #                 ),

    #             lambda success:
    #                 self.download_page.update_finished(
    #                     download_id,
    #                     success
    #                 )
    #         )

            


            
    #Schdule
    def open_schdule_dialog(self):
        print("Oki Schdule")
        # dialog = SchduleDialog(self)
        
    def download_progress(self, progress):
        print("UI Progress:", progress)  
# https://cdn.truefilesize.com/test/test-10mb.bin
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