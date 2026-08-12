# utils/helpers.py
import re
import os
import hashlib

def format_bytes(size_in_bytes: int) -> str:
    """Bytes ပမာဏကို KB, MB, GB, TB သို့ ပြောင်းလဲပေးခြင်း"""
    if not size_in_bytes or size_in_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    size = float(size_in_bytes)
    
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1
        
    return f"{size:.2f} {units[i]}"


def sanitize_filename(filename: str) -> str:
    """Windows/Linux FS တွင် လက်မခံသော စာလုံးများ (\ / : * ? " < > |) ကို ဖယ်ရှားပေးခြင်း"""
    if not filename:
        return "unnamed_file"
    # မကင်းလွတ်သော စာလုံးများကို Underscore (_) ဖြင့် အစားထိုးမည်
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def format_seconds(seconds: int) -> str:
    """စက္ကန့် အရေအတွက်ကို HH:MM:SS ပုံစံသို့ ပြောင်းလဲပေးခြင်း (ETA ပြသရန်)"""
    if not seconds or seconds < 0:
        return "00:00:00"
    
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def calculate_file_hash(filepath: str, algo="md5") -> str:
    """ဖိုင် မပျက်စီးကြောင်းနှင့် နာမည်တူ တကယ်တူ/မတူ စစ်ရန် MD5/SHA256 Hash တွက်ပေးခြင်း"""
    if not os.path.exists(filepath):
        return ""
    
    hash_obj = hashlib.md5() if algo == "md5" else hashlib.sha256()
    with open(filepath, "rb") as f:
        # Memory မပြည့်စေရန် Chunk အလိုက် ဖတ်ရှုမည်
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
            
    return hash_obj.hexdigest()