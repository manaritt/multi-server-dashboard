import random

def generate_server_metrics():
    servers = [
        {"name": "Server-01", "role": "Database Node", "cpu": random.uniform(30, 95), "ram": random.uniform(40, 90), "response_time": random.uniform(10, 50)},
        {"name": "Server-02", "role": "Web Server", "cpu": random.uniform(20, 85), "ram": random.uniform(30, 80), "response_time": random.uniform(8, 35)},
        {"name": "Server-03", "role": "Application Node", "cpu": random.uniform(40, 98), "ram": random.uniform(50, 95), "response_time": random.uniform(15, 80)},
        {"name": "Server-04", "role": "Backup Node", "cpu": random.uniform(10, 60), "ram": random.uniform(20, 70), "response_time": random.uniform(5, 25)},
    ]
    
    for server in servers:
        if server["cpu"] > 85 or server["ram"] > 85:
            server["status"] = "Critical"
        elif server["cpu"] > 70 or server["ram"] > 70:
            server["status"] = "Warning"
        else:
            server["status"] = "Healthy"
            
    return servers

def trigger_auto_healing(server_name, action):
    if action == "clear_cache":
        return f"تم تنظيف الذاكرة المؤقتة لـ {server_name} بنجاح!"
    elif action == "restart":
        return f"تم إرسال أمر إعادة التشغيل لـ {server_name}."
    return "إجراء غير معروف."

if name == "main":
    print(generate_server_metrics())
