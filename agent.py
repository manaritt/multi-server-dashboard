import psutil
import requests
import time
from datetime import datetime

# اسم السيرفر الحالي الذي يعمل عليه هذا السكريبت
SERVER_NAME = "Server-Local-Node"

def get_system_metrics():
    """قراءة موارد السيرفر الحالية"""
    return {
        "server_name": SERVER_NAME,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if name == "main":
    print(f"🚀 بدء مراقبة السيرفر: {SERVER_NAME}...")
    # يقرأ الموارد كل 5 ثوانٍ
    metrics = get_system_metrics()
    print("القراءات الحالية للسيرفر:", metrics)