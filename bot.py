import os
import requests


# Django model integration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto.settings")
try:
    import django
    django.setup()
except Exception:
    pass

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from doc.models import TelegramContact

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
API_URL = os.getenv("API_URL", "https://edumatch1.up.railway.app/api/courses/")


def normalize_phone(value):
    phone = str(value).strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    if not phone.startswith("+"):
        phone = "+" + phone
    return phone


def send_code_to_phone(phone_number, code):
    """Django tomonidan chaqiriladi: saqlangan Telegram chat_id ga kod yuboradi."""
    if not BOT_TOKEN:
        print("BOT_TOKEN topilmadi")
        return False

    contact = TelegramContact.objects.filter(phone_number=normalize_phone(phone_number)).first()
    if not contact:
        print("Telegram contact topilmadi:", phone_number)
        return False

    text = (
        "🔐 <b>EduMatch tasdiqlash kodi</b>\n\n"
        f"Sizning 6 xonali kodingiz: <b>{code}</b>\n\n"
        "Bu kodni EduMatch saytiga kiriting. Kod 5 daqiqa amal qiladi."
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": contact.chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
        return response.ok and response.json().get("ok", False)
    except requests.RequestException as exc:
        print("Telegram API error:", exc)
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Telefon raqamimni ulashish", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "🎓 EduMatch'da login/register qilish uchun avval Telegram hisobingizni ulang.\n\n"
        "Pastdagi tugmani bosib, Telegram'dagi telefon raqamingizni yuboring. "
        "Shundan keyin saytga telefon raqamingizni kiritsangiz, tasdiqlash kodi shu botga keladi.",
        reply_markup=keyboard,
    )


async def save_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        return

    # Faqat foydalanuvchining o'z kontaktini qabul qilamiz.
    if update.effective_user and contact.user_id != update.effective_user.id:
        await update.message.reply_text("❌ Iltimos, o'zingizning Telegram raqamingizni yuboring.")
        return

    phone = normalize_phone(contact.phone_number)
    TelegramContact.objects.update_or_create(
        phone_number=phone,
        defaults={
            "chat_id": update.effective_chat.id,
            "telegram_username": update.effective_user.username or "",
            "first_name": update.effective_user.first_name or "",
        },
    )

    await update.message.reply_text(
        "✅ Telegram hisobingiz EduMatch bilan ulandi!\n\n"
        "Endi saytga telefon raqamingizni kiriting. Tasdiqlash kodi shu chatga keladi.",
    )


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code != 200:
            await query.message.reply_text("❌ Kurslarni olishda xatolik.")
            return
        data = response.json()
        items = data.get("results", []) if isinstance(data, dict) else data
        if not items:
            await query.message.reply_text("📭 Hozircha kurslar mavjud emas.")
            return
        for course in items[:10]:
            text = (
                f"📚 <b>{course.get('title', 'Nomaʼlum kurs')}</b>\n\n"
                f"📂 Yo'nalish: {course.get('category', 'Nomaʼlum')}\n"
                f"👨‍🏫 O'qituvchi: {course.get('teacher', 'Nomaʼlum')}\n"
                f"💰 Narx: {course.get('price', 0):,} so'm\n"
                f"⭐ Reyting: {course.get('rating', 0)}"
            )
            start_time = course.get("start_time")
            end_time = course.get("end_time")
            if start_time and end_time:
                text += f"\n🕐 Vaqt: {str(start_time)[:5]} - {str(end_time)[:5]}"
            await query.message.reply_text(text, parse_mode="HTML")
    except requests.RequestException:
        await query.message.reply_text("❌ Django server bilan bog'lanib bo'lmadi.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "courses":
        await courses(update, context)


def main():
    if not BOT_TOKEN:
        raise ValueError('BOT_TOKEN topilmadi. PowerShell: $env:BOT_TOKEN="TOKEN"')

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, save_contact))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 EduMatch bot ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
