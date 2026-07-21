import os
import json
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004459815440          # آیدی عددی کانال (حتی اگه عمومی باشه فرقی نداره)
DATA_FILE = "/app/data/posts.json"   # مسیر داخل Railway

bot = telebot.TeleBot(TOKEN)

def load_ids():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_post(msg_id):
    ids = load_ids()
    if msg_id not in ids:
        ids.append(msg_id)
        with open(DATA_FILE, "w") as f:
            json.dump(ids, f)

def get_two_random():
    ids = load_ids()
    if len(ids) < 2:
        return []
    return random.sample(ids, 2)

@bot.message_handler(commands=['start'])
def send_posts(message):
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
            bot.reply_to(message, f"خطا: {e}")

@bot.channel_post_handler(func=lambda m: True)
def handle_new_post(message):
    add_post(message.message_id)
    print(f"✅ پست جدید ذخیره شد: {message.message_id}")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده!")
    print("🚀 ربات آماده‌ست...")
    bot.infinity_polling(allowed_updates=["channel_post"])
