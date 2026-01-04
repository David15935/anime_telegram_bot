from telegram import Update
from telegram.ext import ContextTypes
from bot.anime_api import *
from bot.keyboards import anime_buttons
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import uuid

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 *Anime Bot Activated*\n\n"
        "/anime <name>\n"
        "/top\n"
        "/airing\n"
        "/wallpaper",
        parse_mode="Markdown"
    )

async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /anime Naruto")
        return

    data = search_anime(" ".join(context.args))
    if not data:
        await update.message.reply_text("Anime not found.")
        return

    a = data[0]
    trailer = a["trailer"]["url"] or "https://youtube.com"
    mal = a["url"]
    anilist = f"https://anilist.co/search/anime?search={a['title']}"

    text = (
        f"🎌 *{a['title']}*\n"
        f"⭐ Score: {a['score']}\n"
        f"📺 Episodes: {a['episodes']}\n"
        f"📅 Status: {a['status']}\n"
        f"🎭 Genres: {', '.join(g['name'] for g in a['genres'])}\n"
        f"\n📝 {a['synopsis'][:400]}..."
    )

    await update.message.reply_photo(
        photo=a["images"]["jpg"]["large_image_url"],
        caption=text,
        parse_mode="Markdown",
        reply_markup=anime_buttons(trailer, mal, anilist)
    )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = top_anime()
    msg = "🔥 *Top Anime*\n\n"
    for a in data:
        msg += f"⭐ {a['title']} — {a['score']}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def airing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = airing_anime()
    msg = "📡 *Currently Airing*\n\n"
    for a in data:
        msg += f"📺 {a['title']}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = anime_wallpaper()
    await update.message.reply_photo(
    photo=url,
    caption=f"🖼️ Anime Wallpaper\n🎌 {title}"
)

async def inline_search(update, context):
    query = update.inline_query.query

    if not query:
        return

    results = []
    try:
        data = search_anime(query)
    except Exception:
        return

    for anime in data[:5]:
        title = anime["title"]
        score = anime["score"] or "N/A"
        url = anime["url"]

        description = f"⭐ {score} | {anime['status']}"

        message = (
            f"🎌 *{title}*\n"
            f"⭐ Score: {score}\n"
            f"📺 Episodes: {anime['episodes']}\n"
            f"📅 Status: {anime['status']}\n"
            f"\n🔗 {url}"
        )

        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode="Markdown"
                )
            )
        )

    await update.inline_query.answer(results, cache_time=10)

async def inline_search(update, context):
    query = update.inline_query.query

    if not query:
        return

    results = []
    try:
        data = search_anime(query)
    except Exception:
        return

    for anime in data[:5]:
        title = anime["title"]
        score = anime["score"] or "N/A"
        url = anime["url"]

        description = f"⭐ {score} | {anime['status']}"

        message = (
            f"🎌 *{title}*\n"
            f"⭐ Score: {score}\n"
            f"📺 Episodes: {anime['episodes']}\n"
            f"📅 Status: {anime['status']}\n"
            f"\n🔗 {url}"
        )

        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode="Markdown"
                )
            )
        )

    await update.inline_query.answer(results, cache_time=10)
