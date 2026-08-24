from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Nexora")
        self.resize(1200, 700)