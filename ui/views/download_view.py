# ui/views/download_view.py
import tkinter as tk
from tkinter import ttk, filedialog

class DownloadView(ttk.Frame):
    def __init__(self, parent, sync_mgr, db):
        super().__init__(parent)
        self.sync_mgr = sync_mgr
        self.db = db
        self._init_ui()

    def _init_ui(self):
        # 1. Drive Input Section
        input_frame = ttk.LabelFrame(self, text=" Google Drive Target ")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Folder ID/URL:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_drive_id = ttk.Entry(input_frame, width=50)
        self.ent_drive_id.grid(row=0, column=1, padx=5, pady=5)

        # 2. Controls & Actions
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="🔍 Start Scan", command=self._start_scan).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="⏬ Start Download", command=self._start_download).pack(side="left", padx=5)

    def _start_scan(self):
        # Scan Worker ကို ခေါ်ယူမောင်းနှင်မည့် Logic
        pass

    def _start_download(self):
        # Sync Manager မှတစ်ဆင့် Queue ဆောက်ပြီး ဒေါင်းလုဒ်စမည့် Logic
        pass