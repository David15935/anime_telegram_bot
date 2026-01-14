from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    InlineQueryResultArticle, InputTextMessageContent
)
from telegram.ext import ContextTypes
from bot.anime_api import (
    search_anime, get_anime_by_id, get_top_anime,
    get_airing, get_wallpapers
)

# -------------------- START --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Anime Bot!\n\n"
        "Commands:\n"
        "/anime <name> - Get anime details\n"
        "/top - Top anime\n"
        "/airing - Currently airing\n"
        "/wallpaper - Anime wallpapers\n"
        "Or try inline search: type @YourBotName <anime>"
    )

# -------------------- ANIME DETAILS --------------------
async def anime_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /anime <anime name>")
        return

    query = " ".join(context.args)
    try:
        search_result = await search_anime(query)
        if not search_result:
            await update.message.reply_text("❌ Anime not found.")
            return

        mal_id = search_result["mal_id"]
        anime = await get_anime_by_id(mal_id)

        title = anime["title"]
        score = anime.get("score", "N/A")
        episodes = anime.get("episodes", "N/A")
        synopsis = anime.get("synopsis", "No synopsis available.")
        image = anime["images"]["jpg"]["large_image_url"]

        # Trailer
        trailer_url = anime.get("trailer", {}).get("url")
        buttons = []
        if trailer_url:
            buttons.append([InlineKeyboardButton("▶️ Watch Trailer", url=trailer_url)])

        caption = (
            f"🎬 {title}\n"
            f"⭐ Score: {score}\n"
            f"📺 Episodes: {episodes}\n\n"
            f"📖 {synopsis[:800]}..."
        )

        await update.message.reply_photo(
            photo=image,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        )
    except Exception as e:
        await update.message.reply_text("⚠️ Failed to fetch anime details.")
        raise e

# -------------------- TOP ANIME --------------------
async def top_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_anime()
    text = "🏆 Top Anime:\n\n"
    for a in top[:10]:
        text += f"{a['title']} ({a['score']})\n"
    await update.message.reply_text(text)

# -------------------- AIRING --------------------
async def airing_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    airing = await get_airing()
    text = "📺 Currently Airing:\n\n"
    for a in airing[:10]:
        text += f"{a['title']} ({a['score']})\n"
    await update.message.reply_text(text)

# -------------------- WALLPAPERS --------------------
async def wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallpapers = await get_wallpapers()
    page = int(context.user_data.get("wallpaper_page", 0))
    items_per_page = 1

    if page >= len(wallpapers):
        page = 0

    photo_url = wallpapers[page]
    buttons = [
        [
            InlineKeyboardButton("⬅️ Prev", callback_data="wall_prev"),
            InlineKeyboardButton("Next ➡️", callback_data="wall_next"),
        ]
    ]

    await update.message.reply_photo(
        photo=photo_url,
        caption=f"Wallpaper {page+1}/{len(wallpapers)}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def wallpaper_paginate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "wall_next":
        context.user_data["wallpaper_page"] = context.user_data.get("wallpaper_page", 0) + 1
    else:
        context.user_data["wallpaper_page"] = context.user_data.get("wallpaper_page", 0) - 1
    await wallpaper(update=query, context=context)

# -------------------- INLINE SEARCH --------------------
async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    page = int(context.bot_data.get(f"page_{query}", 1))
    results = await search_anime(query)
    items_per_page = 5
    start = (page - 1) * items_per_page
    end = start + items_per_page

    items = []
    for a in results[start:end]:
        items.append(
            InlineQueryResultArticle(
                id=str(a["mal_id"]),
                title=a["title"],
                input_message_content=InputTextMessageContent(
                    f"🎬 {a['title']}\nUse /anime {a['title']} for details!"
                ),
            )
        )

    buttons = []
    if page > 1:
        buttons.append([InlineKeyboardButton("⬅️ Prev", callback_data=f"inline_prev:{query}:{page}")])
    if end < len(results):
        buttons.append([InlineKeyboardButton("Next ➡️", callback_data=f"inline_next:{query}:{page}")])

    await update.inline_query.answer(items, cache_time=1, is_personal=True)

# -------------------- INLINE PAGINATION --------------------
async def paginate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("inline_next:") or data.startswith("inline_prev:"):
        action, anime_query, current_page = data.split(":")
        current_page = int(current_page)
        if action == "inline_next":
            new_page = current_page + 1
        else:
            new_page = current_page - 1

        context.bot_data[f"page_{anime_query}"] = new_page
        await query.edit_message_text(f"Type @YourBotName {anime_query} again to see page {new_page}")
