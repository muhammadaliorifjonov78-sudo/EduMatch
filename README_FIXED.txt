EduMatch backend - fixed media/image/API version

Asosiy tuzatishlar:
- media/ va media/courses/ papkalari qo'shildi.
- MEDIA_URL va MEDIA_ROOT sozlandi.
- DEBUG paytida /media/ URL'lari serve qilinadi.
- Course.image ImageField bilan ishlaydi.
- Pillow requirements.txt ga qo'shildi.
- Django 5.2.17 + DRF 3.17.1 ga mos requirements berildi.
- /api/courses/ GET category/search filtri saqlanadi.
- /api/courses/ POST faqat Manager group, staff yoki superuser uchun.
- Eski kurslarda saqlangan tashqi image URL'lar API orqali to'g'ri qaytariladi.

O'rnatish:
1) PowerShell'da backend papkasiga kiring.
2) python -m pip install -r requirements.txt
3) python manage.py migrate
4) python manage.py createsuperuser  (agar hali admin user yo'q bo'lsa)
5) python manage.py runserver

Admin:
http://127.0.0.1:8000/admin/

Rasm:
Admin -> Course -> Image -> Choose File
Rasm media/courses/ ichiga tushadi.

API:
GET  http://127.0.0.1:8000/api/courses/
GET  http://127.0.0.1:8000/api/courses/?category=Dasturlash
GET  http://127.0.0.1:8000/api/courses/?category=Web%20Dasturlash
GET  http://127.0.0.1:8000/api/courses/?search=python
POST http://127.0.0.1:8000/api/courses/  (Manager/staff/superuser)

Manager:
Admin -> Groups -> Manager guruhini yarating.
Keyin kerakli userga Manager groupini bering.
