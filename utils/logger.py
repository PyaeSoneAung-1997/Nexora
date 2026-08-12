# utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="nexora", log_file="logs/app.log", level=logging.INFO):
    """App တစ်ခုလုံးတွင် သုံးရန် Logger စနစ်ကို တည်ဆောက်ပေးခြင်း"""
    
    # Log Folder မရှိသေးပါက ဆောက်မည်
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Log Message Formatter ( [2026-08-12 10:30:00] [INFO] [gdrive_service]: Scanned 100 files )
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. File ထဲ သို့ သိမ်းမည့် Handler (ဖိုင် size 5MB ပြည့်ပါက အသစ်လဲမည်၊ အများဆုံး 3 ဖိုင်ထိထားမည်)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 2. Console (Terminal) ပေါ်တွင် ပြမည့် Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Handler များ ထည့်သွင်းခြင်း (ထပ်မနေစေရန် စစ်ဆေးပါသည်)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# App တစ်ခုလုံးတွင် import get_logger သုံး၍ ခေါ်သုံးရန်
logger = setup_logger()