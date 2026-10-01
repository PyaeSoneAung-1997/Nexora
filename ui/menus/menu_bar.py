from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Task Menu
        self.task_menu = self.addMenu("Task")

        # Add New Download
        self.add_new_download_action = self.task_menu.addAction(
            "Add New Download"
        )