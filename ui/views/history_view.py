# ui/views/history_view.py
import tkinter as tk
from tkinter import ttk
import os

class HistoryView(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self._init_ui()

    def _init_ui(self):
        # Search Frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search History:").pack(side="left", padx=5)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5)

        # Action Buttons
        ttk.Button(search_frame, text="📂 Open File Directory", command=self._open_file_folder).pack(side="right", padx=5)

        # History Treeview Table
        cols = ("ID", "File Name", "Save Path", "Completed At")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def _open_file_folder(self):
        """ရွေးထားသော ဖိုင်ကျခဲ့သည့် Local Directory ကို Windows Explorer ဖြင့် ဖွင့်ပေးမည်"""
        selected = self.tree.selection()
        if selected:
            file_path = self.tree.item(selected[0])['values'][2] # Save Path
            os.system(f'explorer /select,"{file_path}"')