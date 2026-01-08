from telegram import Update
from telegram.ext import ContextTypes
from bot.anime_api import search_anime, get_anime_by_id


# ---------- INLINE SEARCH (STUB) ----------
async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.inline_query.answer(
        [],
        switch_pm_text="Use /anime <name> for full details",
        switch_pm_parameter="start",
    )


# ---------- ANIME DETAILS ----------
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

        trailer_url = (
            anime["trailer"]["url"]
            if anime.get("trailer") and anime["trailer"]["url"]
            else "No trailer available"
        )

        caption = (
            f"🎬 **{title}**\n\n"
            f"⭐ Score: {score}\n"
            f"📺 Episodes: {episodes}\n\n"
            f"📖 {synopsis[:800]}...\n\n"
            f"▶️ Trailer: {trailer_url}"
        )

        await update.message.reply_photo(
            photo=image,
            caption=caption,
            parse_mode="Markdown",
        )

    except Exception as e:
        await update.message.reply_text("⚠️ Failed to fetch anime details.")
        raise e


# ---------- PAGINATION (STUB) ----------
async def paginate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Pagination coming soon.")
