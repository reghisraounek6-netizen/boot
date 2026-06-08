import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== الإعدادات ====================
BOT_TOKEN = "YOUR_BOT_TOKEN"       # من @BotFather
ADSGRAM_BLOCK_ID = "YOUR_BLOCK_ID" # من adsgram.ai

logging.basicConfig(level=logging.INFO)

# ==================== الأوامر ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # رسالة الترحيب
    await update.message.reply_text(
        f"👋 أهلاً {user.first_name}!\n\n"
        "🤖 أنا بوتك الذكي — اكتب /help لترى ما أقدر أفعله."
    )

    # إرسال الإعلان
    await send_ad(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 الأوامر المتاحة:\n\n"
        "/start — البداية\n"
        "/joke — نكتة عشوائية\n"
        "/quote — اقتباس يومي"
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 سألت الكمبيوتر: كم 1+1؟\n"
        "قال: خطأ! السؤال غير معرّف. 😄"
    )
    await send_ad(update, context)

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *اقتباس اليوم:*\n\n"
        "_\"النجاح ليس نهائياً، والفشل ليس قاتلاً — المهم هو الشجاعة على الاستمرار.\"_\n\n"
        "— ونستون تشرشل",
        parse_mode="Markdown"
    )
    await send_ad(update, context)

# ==================== الإعلان ====================

async def send_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يرسل رابط إعلان Adsgram للمستخدم"""
    user_id = update.effective_user.id

    # رابط الإعلان من Adsgram
    ad_url = f"https://api.adsgram.ai/adv?blockId={ADSGRAM_BLOCK_ID}&tg_id={user_id}"

    keyboard = [[InlineKeyboardButton("📢 شاهد الإعلان واربح", url=ad_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💰 ادعم البوت بمشاهدة إعلان سريع:",
        reply_markup=reply_markup
    )

# ==================== التشغيل ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("quote", quote))

    print("✅ البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
