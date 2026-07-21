import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004459815440

EXISTING_POSTS = [
    165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151,
    150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136,
    135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121,
    120, 119, 118, 117, 116, 1
]

# فعال‌سازی لاگ
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# حافظهٔ موقت برای پست‌های جدید (تا ری‌استارت بعدی)
new_posts = []

def get_two_random():
    all_posts = EXISTING_POSTS + new_posts
    if len(all_posts) < 2:
        return []
    return random.sample(all_posts, 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ids = get_two_random()
    if not ids:
        await update.message.reply_text("هنوز دو پست توی کانال ذخیره نشده. 🙁")
        return
    for msg_id in ids:
        try:
            await update.message.forward_from_chat_id(
                chat_id=CHANNEL_ID,
                message_id=msg_id
            )
        except Exception as e:
            logger.error(f"خطا در فوروارد {msg_id}: {e}")
            await update.message.reply_text(f"خطا در ارسال پست {msg_id}.")

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = len(EXISTING_POSTS) + len(new_posts)
    await update.message.reply_text(f"📊 تعداد پست‌های ذخیره‌شده: {total}")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_id = update.channel_post.message_id
    new_posts.append(msg_id)
    logger.info(f"✅ پست جدید اضافه شد: {msg_id}")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده!")

    app = Application.builder().token(TOKEN).build()

    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("count", count))
    app.add_handler(MessageHandler(filters.ALL, handle_channel_post))

    logger.info("🚀 ربات با موفقیت اجرا شد. برای شروع /start را بزنید.")
    # اجرای polling بدون skip_pending و بدون webhook
    app.run_polling()

if __name__ == "__main__":
    main()
