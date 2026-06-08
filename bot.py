import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import urllib.request
import json

BOT_TOKEN = "8946579180:AAGDJD4WL_8ZNaII7jiD8-27hAOao5HqBfo"  # من @BotFather

logging.basicConfig(level=logging.INFO)

# ==================== البحث عبر API مجاني ====================

def search_anime(query):
    url = f"https://api.jikan.moe/v4/anime?q={urllib.parse.quote(query)}&limit=1"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
            if data["data"]:
                a = data["data"][0]
                return {
                    "title": a.get("title_arabic") or a.get("title"),
                    "score": a.get("score", "؟"),
                    "episodes": a.get("episodes", "؟"),
                    "status": a.get("status", "؟"),
                    "synopsis": (a.get("synopsis") or "")[:200],
                    "url": a.get("url", ""),
                    "image": a.get("images", {}).get("jpg", {}).get("image_url", "")
                }
    except:
        pass
    return None

import urllib.parse

# ==================== الأوامر ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 *أهلاً في بوت الأنميات والأفلام!*\n\n"
        "📋 الأوامر:\n"
        "/anime اسم — ابحث عن أنمي\n"
        "/top — أفضل الأنميات حالياً\n"
        "/seasonal — أنميات الموسم الحالي\n\n"
        "أو فقط أرسل اسم أنمي مباشرة 👇",
        parse_mode="Markdown"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب اسم الأنمي بعد الأمر\nمثال: /anime naruto")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🔍 جاري البحث...")
    result = search_anime(query)

    if result:
        msg = (
            f"🎌 *{result['title']}*\n\n"
            f"⭐ التقييم: {result['score']}/10\n"
            f"📺 الحلقات: {result['episodes']}\n"
            f"📌 الحالة: {result['status']}\n\n"
            f"📝 {result['synopsis']}...\n\n"
            f"🔗 [المزيد على MyAnimeList]({result['url']})"
        )
        if result['image']:
            await update.message.reply_photo(result['image'], caption=msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ لم أجد نتائج، جرب اسماً آخر.")

async def top_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري تحميل القائمة...")
    try:
        url = "https://api.jikan.moe/v4/top/anime?limit=5"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        msg = "🏆 *أفضل 5 أنميات على MyAnimeList:*\n\n"
        for i, a in enumerate(data["data"], 1):
            msg += f"{i}. *{a['title']}* — ⭐ {a.get('score', '؟')}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ حدث خطأ، حاول لاحقاً.")

async def seasonal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 جاري تحميل أنميات الموسم...")
    try:
        url = "https://api.jikan.moe/v4/seasons/now?limit=5"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        msg = "🌸 *أنميات الموسم الحالي:*\n\n"
        for a in data["data"][:5]:
            msg += f"• *{a['title']}* — ⭐ {a.get('score') or 'جديد'}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ حدث خطأ، حاول لاحقاً.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    result = search_anime(query)
    if result:
        msg = (
            f"🎌 *{result['title']}*\n\n"
            f"⭐ {result['score']}/10 | 📺 {result['episodes']} حلقة\n\n"
            f"📝 {result['synopsis']}...\n\n"
            f"🔗 [MyAnimeList]({result['url']})"
        )
        if result['image']:
            await update.message.reply_photo(result['image'], caption=msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ لم أجد نتائج، جرب /top لرؤية الأفضل.")

# ==================== التشغيل ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", search))
    app.add_handler(CommandHandler("top", top_anime))
    app.add_handler(CommandHandler("seasonal", seasonal))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
