from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox

from core.url.url_manager import URLManager
from core.file.file_info_manager import FileInfoManager
from core.database.db_manager import DatabaseManager

from connector.url_controller.url_controller import URLController
from connector.download_controller.download_controller import DownloadController



class ControllerManager(QObject):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        #core
        self.url_manager = URLManager()
        self.file_info_manager = FileInfoManager()
        self.db_manager = DatabaseManager()

        #controllers
        self.url_controller = URLController(
            self.main_window,
            self.url_manager
        )

        self.download_controller = DownloadController(
            self.main_window,
            self.db_manager
        )

        #connect signals
        self.url_controller.url_analyzed.connect(
            self.handle_url_result
        )

    def handle_url_result(self, check):
        print("Url_Check:",check)

        if check["type"] == "direct_file":
            url = check["url"]
            print("Url_Check:","Passed")
            self.file_info(url)
        
        elif check["type"] == "google_drive":
            pass  # Placeholder for future implementation

        elif check["type"] == "website":
            pass  # Placeholder for future implementation

       

    def file_info(self, url):

        info = self.file_info_manager.get_info(url)
        print("Fileinfo:", info)
        if not info["success"]:

            QMessageBox.warning(
                self.main_window,
                "Download Error",
                "Unable to get file information."
            )
            return

        print("Fileinfo:", "Passed")

        self.download(url,info)

    def download(self,url,info):

        print("Download_Controller_Started:")
        # direct download
        self.download_controller.show_direct_download(
            url,
            info
            )
        
    def shutdown(self):

        self.download_controller.shutdown()
    