# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox

# Core Layer Imports
from core.database.db_manager import DatabaseManager
from core.sync.sync_manager import SyncManager

# Views & Dialogs Imports
from ui.views.download_view import DownloadView
from ui.views.queue_view import QueueView
from ui.views.history_view import HistoryView
from ui.views.settings_view import SettingsView
from ui.dialogs.conflict_dialog import ConflictResolverDialog
from ui.dialogs.login_dialog import LoginDialog

class MainWindow(tk.Tk):
    """App တစ်ခုလုံး၏ Main Shell & Controller Class"""
    def __init__(self):
        super().__init__()
        self.title("Nexora - Google Drive Sync & Downloader")
        self.geometry("900x600")
        self.minsize(800, 500)

        # 1. Core Services ကို Initialize လုပ်မည်
        self.db = DatabaseManager()
        self.sync_mgr = SyncManager(db_manager=self.db)

        # 2. UI Layout ကို တည်ဆောက်မည်
        self._init_ui()

        # 3. Global Status Polling စတင်မည်
        self._start_global_polling()

    def _init_ui(self):
        # Top Menu Bar
        self._create_menu_bar()

        # Tabs (Notebook) စနစ် တည်ဆောက်ခြင်း
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Sub-views များကို Tab အဖြစ် ထည့်သွင်းခြင်း
        self.download_view = DownloadView(self.notebook, sync_mgr=self.sync_mgr, db=self.db)
        self.queue_view = QueueView(self.notebook, db=self.db)
        self.history_view = HistoryView(self.notebook, db=self.db)
        self.settings_view = SettingsView(self.notebook, db=self.db)

        self.notebook.add(self.download_view, text=" ⏬ Downloads ")
        self.notebook.add(self.queue_view, text=" 📋 Active Queue ")
        self.notebook.add(self.history_view, text=" 📜 History ")
        self.notebook.add(self.settings_view, text=" ⚙️ Settings ")

        # Bottom Status Bar
        self.status_bar = ttk.Label(self, text="Ready", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=2, pady=2)

    def _create_menu_bar(self):
        menubar = tk.Menu(self)
        
        # Account Menu
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Google Login", command=self.open_login_dialog)
        account_menu.add_separator()
        account_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Account", menu=account_menu)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Resolve File Conflicts", command=self.open_conflict_dialog)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        self.config(menu=menubar)

    def open_login_dialog(self):
        """Login Pop-up ခေါ်ယူခြင်း"""
        dialog = LoginDialog(self, db_manager=self.db)

    def open_conflict_dialog(self):
        """Duplicate Rename Pop-up ခေါ်ယူခြင်း"""
        dialog = ConflictResolverDialog(self, db_manager=self.db)

    def _start_global_polling(self):
        """Status Bar ကို Real-time Update ပေးရန် Polling Logic"""
        # Active Job များ သို့မဟုတ် Download Speeds များကို စက္ကန့်မလပ် စစ်ဆေးမည့်နေရာ
        self.after(1000, self._start_global_polling)