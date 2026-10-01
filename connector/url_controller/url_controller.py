from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox,QDialog
from ui.dialogs.add_url_dialog import AddURLDialog



class URLController(QObject):

    url_analyzed = pyqtSignal(dict)

    def __init__(self, main_window,url_manager):
        super().__init__()

        self.main_window = main_window
        self.url_manager = url_manager

        self._connect_actions()

    def _connect_actions(self):
        # MenuBar
        self.main_window.menu_bar.add_new_download_action.triggered.connect(
            self.handle_add_new_download
        )

        # ToolBar
        self.main_window.tool_bar.add_url_action.triggered.connect(
            self.handle_add_url
        )

    def handle_add_new_download(self):
        print("Add New Download clicked")

    def handle_add_url(self):

            dialog = AddURLDialog(self.main_window)

            result = dialog.exec()

            if result != QDialog.DialogCode.Accepted:
                 return

            url = dialog.url_input.text().strip()

            if not url:

                QMessageBox.warning(
                      dialog,
                      "Invalid URL",
                      "Please enter a URL."
                 )

                self.handle_add_url()
                return
            
            check = self.url_manager.analyze(url)

            if not check["valid"]:
                 QMessageBox.warning(
                      dialog,
                      "Invalid URL",
                      "The URL you entered is valid"
                 )
                 self.handle_add_url()
                 return
            
            self.url_analyzed.emit(check)