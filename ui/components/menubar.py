import tkinter as tk
from tkinter import ttk, messagebox

class CustomMenubar(tk.Frame):
    """Custom Menu Bar Component"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side="top", fill="x")

        self.main_btn_kwargs = {
            "bd": 0,
            "padx": 10,
            "pady": 4,
            "activebackground": "#BBBCBD"
        }

        self.sub_menu_kwargs = {
            "tearoff": 0, 
            "activebackground": "#007acc"
        }

        self.menus_data = {
            "File": [
                ("Resolve File Conflicts", lambda: print("Resolve File Conflicts")),
                ("Exit", self.parent.destroy)
            ],
            "View": [
                ("Zoom In", lambda: print("Zoom In")),
                ("Zoom Out", lambda: print("Zoom Out"))
            ],
            "Download": [
                ("Start All", lambda: print("Start All")),
                ("Pause All", lambda: print("Pause All"))
            ],
            "Setting": [
                ("Preferences", lambda: print("Preferences"))
            ],
            "Help": [
                ("Documentation", lambda: print("Documentation"))
            ],
            "About": [
                ("About App", lambda: print("About App"))
            ]
        }


        for title, items in self.menus_data.items():
            # Menubutton တည်ဆောက်ခြင်း
            btn = tk.Menubutton(self, text=title, **self.main_btn_kwargs)
            btn.pack(side="left")
            
            # Dropdown Sub-menu တည်ဆောက်ခြင်း
            sub_menu = tk.Menu(btn, **self.sub_menu_kwargs)
            
            # Sub-menu ထဲသို့ Item များကို Loop ပတ်၍ ထည့်ခြင်း
            for label, command in items:
                sub_menu.add_command(label=label, command=command)
                
            btn.config(menu=sub_menu)