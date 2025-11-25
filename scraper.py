import requests
from bs4 import BeautifulSoup
import re
import os

# آدرس کانال تلگرام (نسخه وب برای خواندن بدون فیلترشکن در سرور)
url = "https://t.me/s/prrofile_purple"

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # پیدا کردن تمام پیام‌های متنی کانال
    messages = soup.select('.tgme_widget_message_text')
    
    if messages:
        # دریافت متن آخرین پست (فقط پست آخر)
        last_message = messages[-1].get_text()
        
        # الگوی پیدا کردن کانفیگ‌ها (Vless, Vmess, Trojan, SS)
        # این کد متن‌های فارسی و توضیحات اضافی را حذف می‌کند و فقط لینک را برمی‌دارد
        configs = re.findall(r'(vless://[a-zA-Z0-9@.:?=&%\-_#]+|vmess://[a-zA-Z0-9]+|trojan://[a-zA-Z0-9@.:?=&%\-_#]+|ss://[a-zA-Z0-9@.:?=&%\-_#]+)', last_message)
        
        if configs:
            # ذخیره کردن در فایل yasin.txt
            with open('yasin.txt', 'w', encoding='utf-8') as f:
                # هر کانفیگ در یک خط جدید
                f.write('\n'.join(configs))
            print("✅ Configs updated successfully from the last post.")
        else:
            print("⚠️ No configs found in the last post.")
            # اگر می‌خواهی در صورت نبودن کانفیگ، فایل قبلی پاک نشود، خط‌های زیر را حذف کن
            # اما طبق درخواست شما برای آپدیت لحظه‌ای، اگر پست آخر کانفیگ نداشت، فایل خالی یا بدون تغییر می‌ماند.
    else:
        print("❌ Could not find any messages.")

except Exception as e:
    print(f"❌ Error occurred: {e}")
