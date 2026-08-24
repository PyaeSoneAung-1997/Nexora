from PyQt6.QtWidgets import QMainWindow, QPushButton
from pri.app_logic import AppLogic


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.logic = AppLogic()

        self.button = QPushButton("Click Me")
        self.setCentralWidget(self.button)

        self.button.clicked.connect(self.handle_click)

    def handle_click(self):
        result = self.logic.do_something()
        print(result)