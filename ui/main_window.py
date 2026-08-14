# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox

from ui.components.menubar import CustomMenubar
from ui.components.toolbar import CustomToolbar
# Core Layer Imports
# from core.database.db_manager import DatabaseManager
# from core.sync.sync_manager import SyncManager

# Views & Dialogs Imports
# from ui.views.download_view import DownloadView
# from ui.views.queue_view import QueueView
# from ui.views.history_view import HistoryView
# from ui.views.settings_view import SettingsView
# from ui.dialogs.conflict_dialog import ConflictResolverDialog
# from ui.dialogs.login_dialog import LoginDialog

class MainWindow(tk.Tk):
    """App တစ်ခုလုံး၏ Main Shell & Controller Class"""
    def __init__(self):
        super().__init__()
        self.title("Nexora - Google Drive Sync & Downloader")
        self.geometry("900x600")
    
        self.minsize(800, 500)

        self.menubar = CustomMenubar(self)
        self.toolbar = CustomToolbar(self)

        # 1. Core Services ကို Initialize လုပ်မည်
        # self.db = DatabaseManager()
        # self.sync_mgr = SyncManager(db_manager=self.db)

        # 2. UI Layout ကို တည်ဆောက်မည်
        self._init_ui()

        # 3. Global Status Polling စတင်မည်
        self._start_global_polling()

    def _init_ui(self):

        # Tabs (Notebook) စနစ် တည်ဆောက်ခြင်း
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

      
        # Bottom Status Bar
        self.status_bar = ttk.Label(self, text="Ready", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=2, pady=2)

    
    
    def _start_global_polling(self):
        """Status Bar ကို Real-time Update ပေးရန် Polling Logic"""
        # Active Job များ သို့မဟုတ် Download Speeds များကို စက္ကန့်မလပ် စစ်ဆေးမည့်နေရာ
        self.after(1000, self._start_global_polling)