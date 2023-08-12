# TranslateTelegramBot
یک ربات تلگرام برای ترجمه متون ارسالی به انگلیسی و فارسی. 
یک کد ساده برای ساخت ربات تلگرام مترجم:
اول از بات [BotFather](https://t.me/BotFather)  یک توکن میگیرید.
بعد برای سرور می‌تونید توی https://www.pythonanywhere.com/ یک اکانت رایگان بسازید.
بعد توی Bash ماژولها رو نصب کنید:

pip install python-telegram-bot==13.7
pip install --upgrade googletrans==4.0.0-rc1

آنگاه فقط میمونه کد که یک فایل .py میسازید و این کد رو میندازید توش و ران میکنید و خلاص.  به جای این YOUR_TELEGRAM_BOT_TOKEN هم توکنی که از BotFather گرفتید رو بگذارید. و خلاص.
بات پیام ها را یکی یکی به انگلیسی و فارسی ترجمه می‌کند و اگر پیام طولانی تر از ماکزیمم کاراکتر تلگرام باشد غیر از اینکه پیام را به قطعات کوچکتر تقسیم و ارسال می‌کند، همچنین پیام را در قالب یک فایل html ارسال می‌کند.
