from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from bot.anime_api import (
    search_anime,
    get_anime_by_id,
    get_top_anime,
    get_airing_anime,
)


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 Anime Bot Ready!\n\n"
        "/anime <name> — Anime details\n"
        "/top — Top anime\n"
        "/airing — Currently airing\n"
        "/wallpaper <name> — Anime wallpaper\n"
    )


# ---------- /anime ----------
async def anime_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /anime <anime name>")
        return

    query = " ".join(context.args)

    try:
        result = await search_anime(query)
        if not result:
            await update.message.reply_text("Anime not found.")
            return

        anime = await get_anime_by_id(result["mal_id"])

        title = anime["title"]
        score = anime.get("score", "N/A")
        episodes = anime.get("episodes", "N/A")
        synopsis = anime.get("synopsis", "No synopsis available.")
        image = anime["images"]["jpg"]["large_image_url"]

        trailer_url = (
            anime["trailer"]["url"]
            if anime.get("trailer") and anime["trailer"]["url"]
            else None
        )

        caption = (
            f"🎬 *{title}*\n\n"
            f"⭐ Score: {score}\n"
            f"📺 Episodes: {episodes}\n\n"
            f"📖 {synopsis[:900]}..."
        )

        buttons = []
        if trailer_url:
            buttons.append(
                [InlineKeyboardButton("▶ Watch Trailer", url=trailer_url)]
            )

        await update.message.reply_photo(
            photo=image,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        )

    except Exception:
        await update.message.reply_text("Failed to fetch anime details.")


# ---------- /top ----------
async def top_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_top_anime()
    text = "🔥 *Top Anime*\n\n"

    for anime in data[:10]:
        text += f"⭐ {anime['title']} ({anime.get('score', 'N/A')})\n"

    await update.message.reply_text(text, parse_mode="Markdown")


# ---------- /airing ----------
async def airing_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_airing_anime()
    text = "📡 *Currently Airing*\n\n"

    for anime in data[:10]:
        text += f"📺 {anime['title']}\n"

    await update.message.reply_text(text, parse_mode="Markdown")


# ---------- /wallpaper ----------
async def wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /wallpaper <anime name>")
        return

    query = " ".join(context.args)
    result = await search_anime(query)

    if not result:
        await update.message.reply_text("Anime not found.")
        return

    image = result["images"]["jpg"]["large_image_url"]
    await update.message.reply_photo(photo=image)


# ---------- INLINE SEARCH (REAL) ----------
async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    from telegram import InlineQueryResultArticle, InputTextMessageContent

    result = await search_anime(query)
    if not result:
        return

    article = InlineQueryResultArticle(
        id=str(result["mal_id"]),
        title=result["title"],
        description=result.get("synopsis", "")[:100],
        input_message_content=InputTextMessageContent(
            f"/anime {result['title']}"
        ),
        thumb_url=result["images"]["jpg"]["image_url"],
    )

    await update.inline_query.answer([article])


# ---------- CALLBACK (PLACEHOLDER FOR PAGINATION) ----------
async def paginate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Pagination coming next 🚧")
