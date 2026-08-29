import sys
import tkinter as tk
from tkinter import ttk,messagebox,scrolledtext
import time
from config import (
    create_app_directories, 
    APP_DATA_DIR,
    APP_NAME,
    APP_VERSION
)
from core.url.url_manager import URLManager
from core.database.db_manager import DatabaseManager
from core.cloud.auth_manager import GoogleAuthManager
from core.cloud.drive_resolver import DriveResolver
from core.cloud.drive_scanner import DriveScanner
from core.sync.sync_manager import SyncManager

def log(message):
    log_box.config(state="normal")            # Text Box ထဲ စာရေးခွင့်ဖွင့်မည်
    log_box.insert(tk.END, message + "\n")    # စာကြောင်းသစ် ထည့်မည်
    log_box.see(tk.END)                       # အောက်ဆုံး စာကြောင်းဆီ အလိုအလျောက် Scroll ဆင်းမည်
    log_box.config(state="disabled")          # User ပြင်၍ မရအောင် ပြန်ပိတ်မည်
    root.update_idletasks()

def main():
    log_box.config(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.config(state="disabled")

    log("🚀 Initializing Nexora Engine...\n")
    time.sleep(0.5)

    # 1. Folders ဖန်တီးခြင်း
    create_app_directories()
    log("📁 System directories initialized.")
    time.sleep(0.5)

    # 2. Database Initialization
    db = DatabaseManager()
    log("💾 SQLite Database initialized successfully.")
    time.sleep(0.5)

    manager = URLManager()
    result = manager.analyze(entry_url_var.get())
    if result["type"] == "None":
        log(f"⚠️ URL Analysis Result: {result['error']}")
    elif result['type'] != "google_dire":
        log(f"This is Other Link, This operation is no complete.Sorry")
    
        auth_mgr = GoogleAuthManager(db_manager=db)
        active_accounts = auth_mgr.get_active_accounts()
        active_acc_id = None

        if active_accounts:
            log(f"\n🔑 Logged in Accounts ({len(active_accounts)}):")
            for acc in active_accounts:
                acc_id = acc["id"]
                email = acc["email"]
                creds = auth_mgr.get_credentials(account_id=acc_id)
                
                if creds:
                    log(f"   - [{acc_id}] {acc['name']} ({email}) -> Credentials Active & Valid ✅")
                    if not active_acc_id:
                        active_acc_id = acc_id
                else:
                    log(f"   - [{acc_id}] {acc['name']} ({email}) -> Credentials Invalid / Token Missing ❌")
                time.sleep(0.5)
        else:
            log("\n🔒 No active accounts found. Starting Google Login Flow...")
            try:
                account = auth_mgr.login()
                active_acc_id = account["id"]
                log(f"✅ Login Successful for: {account['email']}")
            except Exception as e:
                log(f"❌ Login Failed or Cancelled: {e}")
                time.sleep(0.5)

        log("\n✅ Nexora Core Initialization Complete!\n")
        time.sleep(0.5)
        # 4. URL Resolver Analysis (Safe execution)
        url = entry_url_var.get()

        if active_acc_id:
            
            try:
                resolv = DriveResolver()
                # log(f"act:{active_acc_id}")
                # log(f"url:{url}")
                res = resolv.resolve(active_acc_id, url)
               
                log(f"🔗 URL Result:{res['name']}")
            except Exception as e:
                log(f"⚠️ URL Resolution Exception: {e}")
            time.sleep(0.5)
        # 5. Launch Test UI
        log("\nStart Scanning")
        time.sleep(0.5)

# //   
root = tk.Tk()    
root.title(f"{APP_NAME} v{APP_VERSION} - Smart Downloader")
root.geometry("700x800")
root.resizable(False, False)

menu_bar = tk.Frame(root)
menu_bar.pack(side="top", fill="x")
main_btn_kwargs = {
    "bd": 0,
    "padx": 10,
    "pady": 4,
    "activebackground": "#BBBCBD"
}

sub_menu_kwargs = {
    "tearoff": 0, 
    "activebackground": "#007acc"
}

menus_data = {
    "File": [
        ("Resolve File Conflicts", lambda: print("Resolve File Conflicts")),
        ("Exit", root.destroy)
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


for title, items in menus_data.items():
    # Menubutton တည်ဆောက်ခြင်း
    btn = tk.Menubutton(menu_bar, text=title, **main_btn_kwargs)
    btn.pack(side="left")
    
    # Dropdown Sub-menu တည်ဆောက်ခြင်း
    sub_menu = tk.Menu(btn, **sub_menu_kwargs)
    
    # Sub-menu ထဲသို့ Item များကို Loop ပတ်၍ ထည့်ခြင်း
    for label, command in items:
        sub_menu.add_command(label=label, command=command)
        
    btn.config(menu=sub_menu)

content_frame = ttk.Frame(root)
content_frame.pack(fill="both", expand=True, padx=10, pady=10)

url_label = ttk.Label(content_frame, text = "Input URL :")
url_label.grid(row=0, column=0, padx= 10, pady=8, sticky="w")
entry_url_var = tk.StringVar()
entry_url = ttk.Entry(content_frame, textvariable=entry_url_var, width= 60)
entry_url.grid(row=0, column=1, padx=10 , pady=8, sticky="w")

btn_url = ttk.Button(content_frame,text='Ok',command=main)
btn_url.grid(row=0, column=2, padx=10 , pady=8, sticky="w")

btn_url = ttk.Button(content_frame,text='Cancel',command = root.destroy)
btn_url.grid(row=0, column=3, padx=10 , pady=8, sticky="w")

log_label = ttk.Label(content_frame, text="Console Output Log:")
log_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(30, 2), sticky="w")

log_box = scrolledtext.ScrolledText(content_frame, height=15, width=78, state="disabled", font=("Consolas", 9))
log_box.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="w")

root.mainloop()




