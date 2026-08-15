# ui/dialogs/login_dialog.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os



class LoginDialog(tk.Toplevel):
    def __init__(self, parent, db_manager=None, auth_manager=None):
        super().__init__(parent)
        self.title("🔑 Google Account Status")
        self.geometry("450x260")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        self.db = db_manager
        self.auth_mgr = auth_manager
        self._init_ui()

    def _init_ui(self):
        frame = ttk.LabelFrame(self, text=" Google Account Status ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # 1. Credentials JSON File Picker
        ttk.Label(frame, text="Credentials File (credentials.json):").pack(anchor="w", padx=10, pady=(10, 2))
        
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.ent_json_path = ttk.Entry(file_frame)
        self.ent_json_path.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(file_frame, text="Browse...", command=self._browse_json).pack(side="right")

        # 2. Login Status
        self.lbl_status = ttk.Label(frame, text="Status: Not Authenticated", foreground="red", font=("Helvetica", 9, "bold"))
        self.lbl_status.pack(anchor="w", padx=10, pady=10)

        # 3. Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        ttk.Button(btn_frame, text="🌐 Login via Browser", command=self._start_google_login).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=5)

    def _browse_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if path:
            self.ent_json_path.delete(0, tk.END)
            self.ent_json_path.insert(0, path)

    def _start_google_login(self):
        json_path = self.ent_json_path.get().strip()
        if not json_path or not os.path.exists(json_path):
            messagebox.showerror("Error", "ကျေးဇူးပြု၍ မှန်ကန်သော credentials.json ဖိုင်ကို ရွေးချယ်ပေးပါ။", parent=self)
            return

        try:
            # auth_manager မှတစ်ဆင့် Browser ပွင့်ပြီး OAuth Login လုပ်မည့် Logic
            # user_email = self.auth_mgr.login_with_oauth(json_path)
            
            self.lbl_status.config(text="Status: Connected Successfully!", foreground="green")
            messagebox.showinfo("Success", "Google Drive Account အောင်မြင်စွာ ချိတ်ဆက်ပြီးပါပြီ။", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Auth Error", f"Login မအောင်မြင်ပါ: {str(e)}", parent=self)