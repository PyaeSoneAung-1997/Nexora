from PyQt6.QtWidgets import QMainWindow,QApplication
import sys
from uii import MainWindow

# class MainWindow(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.setup_window()

#     def setup_window(self):
#         self.setWindowTitle("Nexora")
#         self.resize(1200, 700)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())