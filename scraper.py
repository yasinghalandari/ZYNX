import requests
import re
import base64

# آدرس کانال تلگرام (نسخه پیش‌نمایش وب)
CHANNEL_URL = "https://t.me/s/prrofile_purple"
# نام فایلی که می‌خواهید ذخیره شود
OUTPUT_FILE = "yasin.txt"

def fetch_configs():
    print(f"Fetching configs from {CHANNEL_URL}...")
    try:
        response = requests.get(CHANNEL_URL, timeout=10)
        response.raise_for_status()
        content = response.text
        
        # الگوی پیدا کردن کانفیگ‌ها (Vmess, Vless, Trojan, Shadowsocks, Tuic, Hysteria)
        # این الگو کانفیگ‌هایی که با پروتکل شروع می‌شوند را پیدا می‌کند
        pattern = r'(vmess|vless|trojan|ss|tuic|hysteria2?)://[a-zA-Z0-9\-\_\=\@\:\.\?\&\/\#\%\+]+'
        
        configs = re.findall(pattern, content)
        
        # حذف تکراری‌ها
        unique_configs = list(set(configs))
        
        if unique_configs:
            print(f"Found {len(unique_configs)} configs.")
            
            # ذخیره در فایل به صورت خط به خط
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                for config in unique_configs:
                    f.write(config + '\n')
            
            print("Configs saved successfully.")
        else:
            print("No configs found.")
            # اگر کانفیگی پیدا نشد، فایل را خالی نمی‌کنیم تا کانفیگ‌های قبلی از بین نروند
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_configs()
