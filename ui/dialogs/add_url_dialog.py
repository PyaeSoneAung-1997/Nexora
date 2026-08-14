# ui/dialogs/add_url_dialog.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from utils.helpers import center_relative_to_parent

# utils & url_detector ထဲမှ Helper ခေါ်ယူရန်
from core.url.url_detector import detect_url_type 

class AddUrlDialog(tk.Toplevel):
    def __init__(self, parent, sync_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.title("➕ Add Google Drive URL")
       
        
        self.withdraw()
        self.geometry("500x280")
        center_relative_to_parent(self,width=500, height=280)
        self.deiconify()
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.sync_mgr = sync_manager
        self._init_ui()

    def _init_ui(self):
        frame = ttk.LabelFrame(self, text=" Target Drive Information ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # 1. URL / ID Input
        ttk.Label(frame, text="Google Drive Folder / File URL:").pack(anchor="w", padx=10, pady=(10, 2))
        self.ent_url = ttk.Entry(frame, width=10)
        self.ent_url.pack(fill="x", padx=10, pady=5)
        
        # ttk.Button(path_frame,text="Start").pack(side="right")
        # 2. Custom Download Save Path
        ttk.Label(frame, text="Download Destination Path:").pack(anchor="w", padx=10, pady=(10, 2))
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=10, pady=5)
        
        self.ent_save_path = ttk.Entry(path_frame)
        self.ent_save_path.insert(0, "D:/nex") # Default path
        self.ent_save_path.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(path_frame, text="Browse...", command=self._browse_save_path).pack(side="right")

        # 3. Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        ttk.Button(btn_frame, text="🚀 Add & Start Sync", command=self._process_url).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=5)

    def _browse_save_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.ent_save_path.delete(0, tk.END)
            self.ent_save_path.insert(0, folder)

    def _process_url(self):
        raw_url = self.ent_url.get().strip()
        save_path = self.ent_save_path.get().strip()

        if not raw_url:
            messagebox.showwarning("Warning", "Google Drive URL သို့မဟုတ် Folder ID ရိုက်ထည့်ပါ။", parent=self)
            return

        # URL Detector ဖြင့် Folder ID သို့မဟုတ် File ID ခွဲထုတ်ခြင်း
        extracted_id, target_type = detect_url_type(raw_url) # 'folder' or 'file'

        if not extracted_id:
            messagebox.showerror("Invalid URL", "Google Drive URL မမှန်ကန်ပါ။ ကျေးဇူးပြု၍ ပြန်စစ်ပါ။", parent=self)
            return

        # Background Sync Worker သို့ Task လွှဲပေးခြင်း
        # self.sync_mgr.start_new_sync_job(extracted_id, save_path, target_type)
        
        messagebox.showinfo("Success", f"{target_type.capitalize()} ID #{extracted_id} ကို Sync Queue ထဲသို့ ထည့်သွင်းပြီးပါပြီ။", parent=self)
        self.destroy()

    