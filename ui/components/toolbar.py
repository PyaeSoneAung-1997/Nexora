import tkinter as tk
from tkinter import ttk
from ui.dialogs.add_url_dialog import AddUrlDialog

class CustomToolbar(tk.Frame):
    """Menu Bar အောက်တွင် ပေါ်လာမည့် Quick Action Toolbar Component"""
    def __init__(self, parent, on_add_url_callback=None):
        # Toolbar ရဲ့ Background အရောင်နှင့် Border များကို သတ်မှတ်သည်
        super().__init__(parent, bg="#EAEAEA", bd=1, relief="raised")
        self.parent = parent
        self.on_add_url_callback = on_add_url_callback
        self.pack(side="top", fill="x")
       
        self._create_toolbar_buttons()

    def _create_toolbar_buttons(self):
        # 1. Add URL Button (URL သစ်ထည့်ရန်)
        self.btn_add_url = ttk.Button(
            self, text="➕ Add URL", 
            command=self._on_add_url
        )
        self.btn_add_url.pack(side="left", padx=5, pady=4)

        # စီးကြောင်းခြားရန် Vertical Line (Separator)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5, pady=4)

        # 2. Start All Button
        self.btn_start = ttk.Button(
            self, text="▶️ Start All", command=self._on_start_all
        )
        self.btn_start.pack(side="left", padx=2, pady=4)

        # 3. Pause All Button
        self.btn_pause = ttk.Button(
            self, text="⏸️ Pause All", command=self._on_pause_all
        )
        self.btn_pause.pack(side="left", padx=2, pady=4)

        # 4. Delete Completed Button
        self.btn_clear = ttk.Button(
            self, text="🗑️ Clear Finished", command=self._on_clear_finished
        )
        self.btn_clear.pack(side="left", padx=2, pady=4)

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=5, pady=4)

        # 5. Settings Button
        self.btn_settings = ttk.Button(
            self, text="⚙️ Settings", command=self._on_settings
        )
        self.btn_settings.pack(side="left", padx=2, pady=4)

    # --- Button Action Event Handlers ---
    def _on_add_url(self):
        #   """Login Pop-up ခေါ်ယူခြင်း"""
        dialog = AddUrlDialog(self.parent,callback=self.on_add_url_callback)
        return dialog
        # မကြာမီ URL Input Dialog ခေါ်ယူသည့် Logic ထည့်ရန်

    def _on_start_all(self):
        print("Toolbar: Start All Downloads")

    def _on_pause_all(self):
        print("Toolbar: Pause All Downloads")

    def _on_clear_finished(self):
        print("Toolbar: Clear Finished Tasks")

    def _on_settings(self):
        print("Toolbar: Open Settings")

  
  