from PyQt6.QtWidgets import QMainWindow

from ui.menus.menu_bar import MenuBar
from ui.widgets.tool_bar import ToolBar

from connector.controller_manager.controller_manager import ControllerManager

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nexora Download Manager")
        self.resize(1000, 700)

        # MenuBar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # ToolBar
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)

        #connector
        self.controller_manager = ControllerManager(self)
        
    def closeEvent(self, event):

        self.controller_manager.shutdown()

        event.accept()