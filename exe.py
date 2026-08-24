print("Online")
print("Offline")
# from ui.main_menu.menu import menu
from ui.main_window import MainWindow

# import tkinter as tk
# from tkinter import ttk, messagebox
from ui.components.menubar import CustomMenubar
from ui.components.toolbar import CustomToolbar

from qr import AddURLDialog

from PyQt6.QtWidgets import QApplication

import sys

def main():

    # root = tk.Tk()

    # root.title("Test")
    # main_window = LoginDialog(root)
    # print(main_window)
    # main_window = AddUrlDialog(root)
    main_window = AddURLDialog()
    return main_window

    app = MainWindow(
        menubar_cls=CustomMenubar,
        toolbar_cls=CustomToolbar
    )
    return app



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app = main()
    # app.mainloop()
