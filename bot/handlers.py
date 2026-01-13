from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import ContextTypes
from bot.anime_api import (
    search_anime,
    get_anime_by_id,
    top_anime,
    airing_anime,
)

# ---------- BASIC COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot online.\n\n"
        "Commands:\n"
        "/anime <name>\n"
        "/top\n"
        "/airing\n"
        "/wallpaper <name>\n\n"
        "You can also use inline search: @YourBotName Naruto"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# ---------- ANIME DETAILS ----------

async def anime_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /anime <anime name>")
        return

    query = " ".join(context.args)
    results = await search_anime(query)

    if not results:
        await update.message.reply_text("Anime not found.")
        return

    anime = await get_anime_by_id(results[0]["mal_id"])

    title = anime["title"]
    synopsis = (anime.get("synopsis") or "No synopsis")[:800]
    image = anime["images"]["jpg"]["large_image_url"]

    buttons = []

    trailer = anime.get("trailer", {}).get("url")
    if trailer:
        buttons.append([InlineKeyboardButton("▶ Trailer", url=trailer)])

    await update.message.reply_photo(
        photo=image,
        caption=f"{title}\n\n{synopsis}",
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )

# ---------- TOP ----------

async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await top_anime()
    text = "🔥 Top Anime:\n\n"
    for a in data:
        text += f"- {a['title']} ⭐ {a.get('score','N/A')}\n"
    await update.message.reply_text(text)

# ---------- AIRING ----------

async def airing_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await airing_anime()
    text = "📺 Currently Airing:\n\n"
    for a in data:
        text += f"- {a['title']}\n"
    await update.message.reply_text(text)

# ---------- WALLPAPER ----------

async def wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /wallpaper <anime name>")
        return

    results = await search_anime(" ".join(context.args))
    if not results:
        await update.message.reply_text("Not found.")
        return

    img = results[0]["images"]["jpg"]["large_image_url"]
    await update.message.reply_photo(photo=img)

# ---------- INLINE SEARCH ----------

async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    results = await search_anime(query)
    answers = []

    for anime in results:
        answers.append(
            InlineQueryResultArticle(
                id=str(anime["mal_id"]),
                title=anime["title"],
                input_message_content=InputTextMessageContent(
                    f"/anime {anime['title']}"
                ),
            )
        )

    await update.inline_query.answer(answers, cache_time=5)
