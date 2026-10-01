from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMovable(False)
        self.setFloatable(False)

        self.setFixedHeight(180)

        self.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        self.add_url_action = self.addAction(
            QIcon("resources/icons/add_url.png"),
            "Add URL"
        )

        self.pause_action = self.addAction(
            QIcon("resources/icons/pause.png"),
            "Pause"
        )

        self.resume_action = self.addAction(
            QIcon("resources/icons/resume.png"),
            "Resume"
        )

        self.stop_action = self.addAction(
            QIcon("resources/icons/stop.png"),
            "Stop"
        )

        self.stop_all_action = self.addAction(
            QIcon("resources/icons/stop_all.png"),
            "Stop All"
        )

        self.delete_action = self.addAction(
            QIcon("resources/icons/delete.png"),
            "Delete"
        )

        self.schdule_action = self.addAction(
            QIcon("resources/icons/schdule.png"),
            "Schdule"
        )

        self.options_action = self.addAction(
            QIcon("resources/icons/options.png"),
            "Options"
        )