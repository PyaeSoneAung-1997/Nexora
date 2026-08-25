from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QIcon,QAction

class toolbar(QToolBar):
    def __init__ (self,main_window):

        super().__init__("Main Toolbar",main_window)      
        self.main_window = main_window
        self.setup()

    def setup(self):

            self.setIconSize(QSize(32, 32))

            self.setMovable(False)

            self.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
            )
            

            self.add_url_action = QAction(
                QIcon("icon/add_url.png"),
                "Add URL", self.main_window
            )

            self.addAction(
                self.add_url_action
            )

            
            self.resume_action = self.addAction(
                QIcon("icon/resume.png"),
                "Resume"
            )

            self.pause_action = self.addAction(
                QIcon("icon/pause.png"),
                "Pause"
            )
            
            self.stop_action = self.addAction(
                QIcon("icon/stop.png"),
                "Stop"
            )

            self.stop_all_action = self.addAction(
                QIcon("icon/stop_all.png"),
                "Stop All"
            )  

            self.delete_action = self.addAction(
                QIcon("icon/delete.png"),
                "Delete"
            )

            self.options_action = self.addAction(
                QIcon("icon/options.png"),
                "Options"
            )

            self.schdule_action = self.addAction(
                QIcon("icon/schdule.png"),
                "Schdule"
            )

            self.addAction(
                self.schdule_action
            )
      

            for action in [
            self.add_url_action,
            self.resume_action,
            self.pause_action,
            self.stop_action,
            self.stop_all_action,
            self.delete_action,
            self.options_action,
            self.schdule_action
            ]:
                button = self.widgetForAction(action)

                if button:
                    button.setFixedSize(70, 70)
        

           

