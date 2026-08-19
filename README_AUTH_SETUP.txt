EDUMATCH TELEGRAM SMS-LIKE VERIFICATION SETUP

1) Telegram botni ishga tushiring. BOT_TOKEN ni PowerShell'da o'rnating:
   $env:BOT_TOKEN="BOTFATHER_DAN_OLINGAN_TOKEN"

2) Backend papkasida:
   python manage.py migrate

3) Django server:
   python manage.py runserver

4) Alohida PowerShell oynasida bot:
   python bot.py

5) Foydalanuvchi avval Telegram'da EduMatch botiga /start yuboradi.
   Bot "Telefon raqamimni ulashish" tugmasini ko'rsatadi. Foydalanuvchi o'z Telegram raqamini ulashadi.

6) Saytda Register yoki Login: +998... telefon raqami va parol.
   Backend TelegramContact orqali shu raqamga mos chat_id ni topadi va 4 xonali kod yuboradi.

7) Verify sahifasida kod to'g'ri bo'lsa backend token beradi va Vue /home ga o'tkazadi.
   Noto'g'ri yoki 5 daqiqadan eski kod bilan Home'ga kirish mumkin emas.

MUHIM:
- Telegram bot oddiy telefon raqamiga o'zi birinchi bo'lib xabar yubora olmaydi. Foydalanuvchi botni /start qilishi va telefonini Contact sifatida ulashishi shart.
- Avvalgi token chatda ochiq ko'rsatilgan bo'lsa, xavfsizlik uchun BotFather orqali tokenni yangilang va yangi tokenni BOT_TOKEN sifatida ishlating.
