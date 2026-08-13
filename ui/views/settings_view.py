# ui/views/settings_view.py
import tkinter as tk
from tkinter import ttk, filedialog

class SettingsView(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self._init_ui()

    def _init_ui(self):
        frame = ttk.LabelFrame(self, text=" Downloader & System Configurations ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Download Path Setting
        ttk.Label(frame, text="Default Download Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ent_path = ttk.Entry(frame, width=40)
        self.ent_path.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(frame, text="Browse...", command=self._browse_path).grid(row=0, column=2, padx=5, pady=10)

        # Threads Setting
        ttk.Label(frame, text="Max Concurrent Downloads:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.spn_threads = ttk.Spinbox(frame, from_=1, to=16, width=10)
        self.spn_threads.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Save Button
        ttk.Button(frame, text="💾 Save Preferences", command=self._save_config).pack(side="bottom", anchor="e", padx=10, pady=10)

    def _browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.ent_path.delete(0, tk.END)
            self.ent_path.insert(0, path)

    def _save_config(self):
        # Settings များကို Database/JSON ထဲ သွားရောက် Update လုပ်မည့် Logic
        pass
