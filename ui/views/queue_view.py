# ui/views/queue_view.py
import tkinter as tk
from tkinter import ttk

class QueueView(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self._init_ui()

    def _init_ui(self):
        # Queue Items Table View
        cols = ("ID", "File Name", "Size", "Progress", "Speed", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_queue_list(self):
        """download_items Table ထဲမှ active queue များကို ဆွဲထုတ်ပြီး Table ကို Update လုပ်မည်"""
        items = self.db.fetch_all("SELECT id, drive_file_id, status FROM download_items WHERE status != 'completed'")
        # Treeview ကို Clear လုပ်ပြီး Data အသစ်ပြန်ဖြည့်မည့် Logic
        pass