import os
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004459815440

# لیست کامل آیدی پست‌ها (همان ۵۱ عددی که فرستادی)
EXISTING_POSTS = [165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 1]

bot = telebot.TeleBot(TOKEN)

# لیست پست‌های جدید (که بعد از اجرا اضافه می‌شوند)
new_posts = []

def get_two_random():
    all_posts = EXISTING_POSTS + new_posts
    if len(all_posts) < 2:
        return []
    return random.sample(all_posts, 2)

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
    new_posts.append(message.message_id)
    print(f"✅ پست جدید اضافه شد: {message.message_id}")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده!")
    print("🚀 ربات با موفقیت اجرا شد. برای شروع /start را بزنید.")
    bot.infinity_polling(allowed_updates=["channel_post"])
