from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QDialog,QMessageBox

from ui.dialogs.direct_download_dialog import DirectDownloadDialog
from ui.dialogs.download_progress_dialog import DownloadProgressDialog
from ui.dialogs.download_complete_dialog import DownloadCompleteDialog
from core.downloads.download_manager import DownloadManager


class DownloadController(QObject):   

    # download_requested = pyqtSignal(dict)

    def __init__(self, main_window, db_manager):
        super().__init__()

        self.db = db_manager
        self.main_window = main_window
        self.download_manager = DownloadManager(self.db)
        
        self.direct_dialog = None
        self.progress_dialog = None

        self.current_download_id = None
        self.current_gid = None
        
        # self._connect_actions()

        # Manager → Controller
        self.download_manager.progress_changed.connect(
            self.handle_progress
        )

        self.download_manager.download_completed.connect(
            self.handle_completed
        )

        self.download_manager.download_error.connect(
            self.handle_error
        )

        
      

    # def _connect_actions(self):

    #     self.main_window.tool_bar.pause_action.triggered.connect(
    #         self.handle_pause
    #     )

    #     self.main_window.tool_bar.resume_action.triggered.connect(
    #         self.handle_resume
    #     )

    #     self.main_window.tool_bar.stop_all_action.triggered.connect(
    #         self.handle_stop_all
        # )

    def show_direct_download(self, url, info):

        self.direct_dialog = DirectDownloadDialog(
            url,
            info,
            self.main_window
        )

        self.direct_dialog.download_requested.connect(
            self.handle_download
        )
        
        result = self.direct_dialog.exec()

        if result != QDialog.DialogCode.Accepted:
            self.direct_dialog = None
            return

        self.direct_dialog = None

    def handle_download(self, data):

        print("Download requested:")
        print(data)

        self.progress_dialog = DownloadProgressDialog(
                    data["filename"],
                    self.main_window
                )
        
        self.progress_dialog.show()


        self.progress_dialog.pause_requested.connect(
                    self.pause_request
                )
        
        self.progress_dialog.resume_requested.connect(
                    self.resume_request
                )   
        
        self.progress_dialog.cancel_requested.connect(
                    self.remove_request
                )   
                
        print("Download_Manager_Started:")

        result = self.download_manager.start_download(data)    
          

        if not result["success"]:
            self.progress_dialog.close()
            self.progress_dialog = None
            QMessageBox.warning(
                self.main_window,
                "Download Error",
                result['error']
            )

            return
        self.current_download_id = result["download_id"]
        self.current_gid = result["aria2_gid"]

        print("Download ID:", self.current_download_id)
        print("Aria2 GID:", self.current_gid)

        
        # print("Download request accepted.")
        
        # self.download_requested.emit(data)

        if self.direct_dialog is not None:
            self.direct_dialog.accept()

    # def handle_pause(self):
    #     print("Pause clicked")

    # def handle_resume(self):
    #     print("Resume clicked")

    # def handle_stop_all(self):
    #     print("Stop All clicked")

    def handle_progress(self, data):

        print("Manager_Emit_Progress_Data")
        print("Controllerr_Received_Prgress")
        print(data)

        if self.progress_dialog is not None:
            self.progress_dialog.update_progress(
                progress=data["progress"],
                downloaded_bytes=data["downloaded_bytes"],
                total_bytes=data["total_size"],
                speed=data["speed"],
                time_left="--",
                connections=data["connections"],
                status=data["status"]
            )

    def handle_completed(self, data):
        print("Manager_Emit_Complete_Data")
        print("Controller_Received_Complete_Data")
        print(data)
        # self.complete_dialog = DownloadCompleteDialog(
        #     data,
        #     self.main_window
        # )

    def handle_error(self, data):
        print("Manager_Emit_Error_Data")
        print("Controller_Received_Error_Data")
        print(data)
        pass
        

    def pause_request(self):
        self.download_manager.pause(self.current_gid)
        print(self.current_gid)
        print("Controller Pause Requested")

    def resume_request(self):
        self.download_manager.resume(self.current_gid)
        print(self.current_gid)
        print("Controller Resume Requested")

    def remove_request(self):
        self.download_manager.remove(self.current_gid)
        print("Controller Remove Requested")

    def shutdown(self):

        self.download_manager.shutdown()