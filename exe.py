# from ui.main_menu.menu import menu
from ui.main_window import MainWindow

import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.login_dialog import LoginDialog
from ui.dialogs.add_url_dialog import AddUrlDialog




def main():
    root = tk.Tk()

    root.title("Test")
    main_window = LoginDialog(root)
    print(main_window)
    main_window = AddUrlDialog(root)
    # main_window = MainWindow()
    return main_window


if __name__ == "__main__":
    app = main()
    app.mainloop()
