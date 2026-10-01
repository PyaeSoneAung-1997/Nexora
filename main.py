import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.windows.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon("resources/icons/Nexora_logo.ico")
    )

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()