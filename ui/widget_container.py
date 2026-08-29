from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from ui.widget.download_item_widget import (
    DownloadItemWidget
)


class DownloadPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.download_layout = QVBoxLayout(self)        

        self.download_widgets = {}

    def add_download( self, download_id, file_name):

        widget = DownloadItemWidget(
            download_id,
            file_name,
            self
        )

        self.download_layout.addWidget(
            widget
        )

        self.download_widgets[
            download_id
        ] = widget

 
        return widget

    def update_progress(self, download_id, data):
        widget = self.download_widgets.get(
            download_id
        )

        if widget:
            widget.update_download_info(
                data
            )

    def update_finished(
            self, download_id, success
    ):
        widget = self.download_widgets.get(
            download_id
        )
        if not widget:
            return

        if success:
            widget.set_completed()

        else:
            widget.set_failed(
                "Download failed"
            )
        
        