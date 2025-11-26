hereimport requests
from bs4 import BeautifulSoup
import re
import os

# آدرس کانال تلگرام (نسخه وب)
url = "https://t.me/s/prrofile_purple"

# فایل خروجی
output_file = "yasin.txt"

def scrape_telegram():
    print(f"Checking {url} ...")
    
    try:
        # دریافت محتوای سایت با هدر مناسب برای جلوگیری از بلاک شدن
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن باکس پیام‌های تلگرام
        messages = soup.find_all('div', class_='tgme_widget_message_text')
        
        found_configs = []
        
        # کلیدواژه‌هایی که دنبالشان هستیم
        keywords = ["vless://", "vmess://", "ss://", "trojan://", "tuic://", "hysteria2://"]

        # بررسی پیام‌ها (از جدید به قدیم یا برعکس مهم نیست چون همش سیو میشه)
        for msg in messages:
            text = msg.get_text(separator="\n") # دریافت متن پیام
            
            # چک می‌کنیم آیا یکی از کلیدواژه‌ها داخل متن هست؟
            if any(key in text for key in keywords):
                # اضافه کردن خط جداکننده برای خوانایی بهتر
                found_configs.append("--------------------------------------------------")
                found_configs.append(text)
                found_configs.append("--------------------------------------------------\n")

        # اگر کانفیگی پیدا شد، در فایل ذخیره کن
        if found_configs:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(found_configs))
            print(f"Success! {len(found_configs)//3} configs saved to {output_file}")
        else:
            print("No configs found in the last messages.")
            # اگر می‌خواهید حتی در صورت پیدا نشدن فایل خالی شود، خط زیر را فعال کنید:
            # open(output_file, "w").close()

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    scrape_telegram()
