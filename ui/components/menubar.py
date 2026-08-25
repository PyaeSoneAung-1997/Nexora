from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar
class menubar(QMenuBar):
        def __init__(self,main_window):
                super().__init__(main_window)
                self.main_window = main_window
                self.setup()                

        def setup(self):
                

                #File
                file_menu = self.addMenu("File")

                self.new_action = QAction(
                        "New", self.main_window
                )

                self.new_action.triggered.connect(
                        self.main_window.new_file
                )
                file_menu.addAction(
                        self.new_action
                )



                
                # self.new_action = file_menu.addAction("New")
                # self.open_action = file_menu.addAction("Open")
                # file_menu.addSeparator()
                # self.exit_action = file_menu.addAction("Exit")

                # # Edit
                # edit_menu = menu_bar.addMenu("Edit")

                # edit_menu.addAction("Undo")
                # edit_menu.addAction("Redo")

                # # View
                # view_menu = menu_bar.addMenu("View")

                # view_menu.addAction("Sidebar")
                # view_menu.addAction("Toolbar")

                # # Help
                # help_menu = menu_bar.addMenu("Help")
                
                # self.about_action = help_menu.addAction("About")

