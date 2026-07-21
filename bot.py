import os
import random
import logging
import telebot

# ------------------- تنظیمات -------------------
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004459815440

# لیست ۵۱ پست اولیه (از قبل استخراج‌شده)
EXISTING_POSTS = [
    165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151,
    150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136,
    135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121,
    120, 119, 118, 117, 116, 1
]
# -------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

# لیست پست‌های جدیدی که بعد از روشن شدن ربات به کانال اضافه می‌شوند
new_posts = []

def get_two_random():
    all_posts = EXISTING_POSTS + new_posts
    if len(all_posts) < 2:
        return []
    return random.sample(all_posts, 2)

@bot.message_handler(commands=['start'])
def send_random_posts(message):
    ids = get_two_random()
    if not ids:
        bot.reply_to(message, "هنوز دو پست توی کانال ذخیره نشده. 🙁")
        return
    for msg_id in ids:
        try:
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
        except Exception as e:
            logger.error(f"خطا در فوروارد پست {msg_id}: {e}")
            bot.reply_to(message, f"خطا در ارسال یکی از پست‌ها (ID: {msg_id}).")

@bot.message_handler(commands=['count'])
def show_count(message):
    total = len(EXISTING_POSTS) + len(new_posts)
    bot.reply_to(message, f"📊 تعداد پست‌های فعلی: {total}")

@bot.channel_post_handler(func=lambda m: True)
def handle_new_post(message):
    new_posts.append(message.message_id)
    logger.info(f"✅ پست جدید اضافه شد: {message.message_id}")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده!")
    # حذف وبهوک و رد شدن از آپدیت‌های قدیمی (کمک به جلوگیری از خطای ۴۰۹)
    bot.remove_webhook()
    logger.info("🚀 ربات با موفقیت اجرا شد. برای شروع /start را بزنید.")
    bot.infinity_polling(allowed_updates=["channel_post"], skip_pending=True)
