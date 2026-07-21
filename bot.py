import os
import json
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004459815440
DATA_FILE = "posts.json"

bot = telebot.TeleBot(TOKEN)

# ---------- ابزارهای ذخیره ----------
def load_ids():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_ids(ids):
    with open(DATA_FILE, "w") as f:
        json.dump(ids, f)

def add_post(msg_id):
    ids = load_ids()
    if msg_id not in ids:
        ids.append(msg_id)
        save_ids(ids)

def get_two_random():
    ids = load_ids()
    if len(ids) < 2:
        return []
    return random.sample(ids, 2)

# ---------- /start ----------
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
            bot.reply_to(message, "خطا در ارسال یکی از پست‌ها. 😕")
            print(e)

# ---------- /check (تست دسترسی) ----------
@bot.message_handler(commands=['check'])
def check_channel(message):
    try:
        # تلاش برای ارسال یک پیام تست به کانال
        test_msg = bot.send_message(CHANNEL_ID, "🟢 تست ربات: دسترسی به کانال برقرار است.")
        # پیام رو بلافاصله پاک می‌کنیم که کانال شلوغ نشه
        bot.delete_message(CHANNEL_ID, test_msg.message_id)
        bot.reply_to(message, "✅ ربات به کانال دسترسی دارد و می‌تواند پیام ارسال کند. آیدی کانال: " + str(CHANNEL_ID))
    except Exception as e:
        bot.reply_to(message, f"❌ خطا در دسترسی به کانال:\n{e}")

# ---------- ذخیره پست‌های کانال ----------
@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    add_post(message.message_id)
    print(f"✅ پست جدید ذخیره شد: {message.message_id}")

# ---------- اجرا ----------
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("لطفاً متغیر محیطی BOT_TOKEN را تنظیم کنید.")
    print("🚀 ربات (telebot) آماده‌ست. منتظر پست‌های جدید و /start ...")
    bot.infinity_polling()import os
import json
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")            # توکن از Railway میاد
CHANNEL_ID = -1004459815440               # آیدی عددی کانال خصوصی
DATA_FILE = "posts.json"

bot = telebot.TeleBot(TOKEN)

# --- ابزارهای ذخیره‌سازی ---
def load_ids():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_ids(ids):
    with open(DATA_FILE, "w") as f:
        json.dump(ids, f)

def add_post(msg_id):
    ids = load_ids()
    if msg_id not in ids:
        ids.append(msg_id)
        save_ids(ids)

def get_two_random():
    ids = load_ids()
    if len(ids) < 2:
        return []
    return random.sample(ids, 2)

# --- دستور /start ---
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
            bot.reply_to(message, "خطا در ارسال یکی از پست‌ها. 😕")
            print(e)

# --- ذخیره‌ی پست‌های کانال ---
@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    add_post(message.message_id)
    print(f"✅ پست جدید ذخیره شد: {message.message_id}")

# --- اجرا ---
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("لطفاً متغیر محیطی BOT_TOKEN را تنظیم کنید.")
    print("🚀 ربات (telebot) آماده‌ست. منتظر پست‌های جدید و /start ...")
    bot.infinity_polling()
