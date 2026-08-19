# from ui.main_menu.menu import menu
from ui.main_window import MainWindow

# import tkinter as tk
# from tkinter import ttk, messagebox
from ui.components.menubar import CustomMenubar
from ui.components.toolbar import CustomToolbar




def main():
    app = MainWindow(
        menubar_cls=CustomMenubar,
        toolbar_cls=CustomToolbar
    )
    return app


if __name__ == "__main__":
    app = main()
    app.mainloop()
