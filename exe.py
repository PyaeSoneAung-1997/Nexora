from PyQt6.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow

from config import (
    create_app_directories, 
    APP_DATA_DIR,
    APP_NAME,
    APP_VERSION
)
# from core.database.db_manager import DatabaseManager

def main():
    # create_app_directories()
    # db = DatabaseManager()
    # print("💾 SQLite Database initialized successfully.")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()