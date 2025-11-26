import requests
from bs4 import BeautifulSoup
import os

# آدرس کانال تلگرام (نسخه وب)
url = "https://t.me/s/prrofile_purple"

# نام فایلی که خواسته بودید
output_file = "yasin.text"

def scrape_telegram():
    print(f"Checking {url} ...")
    
    try:
        # تنظیمات مرورگر برای اینکه تلگرام ما را ربات تشخیص ندهد
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن متن پیام‌ها
        messages = soup.find_all('div', class_='tgme_widget_message_text')
        
        found_configs = []
        
        # کلیدواژه‌هایی که دنبالشان هستیم
        keywords = ["vless://", "vmess://", "ss://", "trojan://", "tuic://", "hysteria2://"]

        # بررسی پیام‌ها
        for msg in messages:
            text = msg.get_text(separator="\n")
            
            # اگر یکی از کلیدواژه‌ها داخل متن بود، کل متن را بردار
            if any(key in text for key in keywords):
                found_configs.append("--------------------------------------------------")
                found_configs.append(text)
                found_configs.append("--------------------------------------------------\n")

        # ذخیره در فایل yasin.text
        if found_configs:
            # حالت 'w' یعنی هر بار فایل قبلی پاک شود و جدیدها نوشته شود
            # اگر می‌خواهید به قبلی‌ها اضافه شود، 'w' را به 'a' تغییر دهید
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(found_configs))
            print(f"Success! configs saved to {output_file}")
        else:
            print("No configs found.")
            # ساخت فایل خالی برای جلوگیری از ارور
            if not os.path.exists(output_file):
                open(output_file, "w").close()

    except Exception as e:
        print(f"Error: {e}")
        # ساخت فایل خالی در صورت ارور برای جلوگیری از شکستن ورک‌فلو
        if not os.path.exists(output_file):
            open(output_file, "w").close()

if __name__ == "__main__":
    scrape_telegram()
