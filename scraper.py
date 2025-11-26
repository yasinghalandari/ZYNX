import requests
from bs4 import BeautifulSoup
import re
import os

# آدرس کانال تلگرام
URL = "https://t.me/s/prrofile_purple"
OUTPUT_FILE = "yasin.text"

def scrape_vless():
    try:
        print(f"Fetching {URL}...")
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        messages = soup.select('.tgme_widget_message_text')
        
        new_configs = []
        
        # استخراج کانفیگ‌ها از پیام‌های کانال
        # پیام‌ها در صفحه معمولا از قدیم به جدید هستند، پس ما لیست رو برعکس میکنیم
        # تا اول پیام‌های آخر (جدیدترین) رو پردازش کنیم
        for msg in reversed(messages):
            text = msg.get_text()
            
            if "vless://" in text:
                # استخراج لینک‌های vless با Regex دقیق
                found_vless = re.findall(r'vless://[a-zA-Z0-9@.:?=&%#_/-]+', text)
                for vless in found_vless:
                    clean_vless = vless.strip()
                    # اگر در لیست جدیدها نبود اضافه کن (جلوگیری از تکرار در یک اجرا)
                    if clean_vless not in new_configs:
                        new_configs.append(clean_vless)

        # خواندن کانفیگ‌های قدیمی از فایل (اگر فایل وجود داشته باشد)
        old_configs = []
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                # خط به خط میخوانیم و فاصله‌ها رو حذف میکنیم
                old_configs = [line.strip() for line in f.readlines() if line.strip()]

        # ترکیب لیست جدید و قدیم
        # هدف: کانفیگ‌های جدید در بالای فایل باشند و تکراری‌ها حذف شوند
        final_list = []
        
        # ۱. اول جدیدها رو اضافه کن (اگر قبلا در فایل نبوده باشند)
        count_added = 0
        for cfg in new_configs:
            if cfg not in old_configs:
                final_list.append(cfg)
                count_added += 1
        
        # ۲. حالا قدیمی‌ها رو که الان گرفتیم اضافه کن (حفظ تاریخچه)
        final_list.extend(old_configs)

        # ذخیره در فایل
        if count_added > 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                for config in final_list:
                    f.write(config + '\n')
            print(f"Update Complete! Added {count_added} new configs. Total: {len(final_list)}")
        else:
            print("No new configs found compared to existing file.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_vless()
