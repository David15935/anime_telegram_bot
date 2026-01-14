import logging
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    InlineQueryHandler, CallbackQueryHandler
)
from config.config import BOT_TOKEN
from bot.handlers import (
    start, anime_details, top_anime,
    airing_anime, wallpaper, inline_search,
    paginate, wallpaper_paginate
)

# -------------------- LOGGING --------------------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------- ERROR HANDLER --------------------
async def error_handler(update, context):
    logger.exception("Unhandled exception while handling an update", exc_info=context.error)

# -------------------- REGISTER COMMANDS --------------------
async def set_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("anime", "Get anime details"),
        BotCommand("top", "Top rated anime"),
        BotCommand("airing", "Currently airing anime"),
        BotCommand("wallpaper", "Anime wallpaper"),
    ]
    await app.bot.set_my_commands(commands)

# -------------------- MAIN --------------------
def main():
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime_details))
    app.add_handler(CommandHandler("top", top_anime))
    app.add_handler(CommandHandler("airing", airing_anime))
    app.add_handler(CommandHandler("wallpaper", wallpaper))

    # Inline & callback handlers
    app.add_handler(InlineQueryHandler(inline_search))
    app.add_handler(CallbackQueryHandler(paginate, pattern="^inline_"))
    app.add_handler(CallbackQueryHandler(wallpaper_paginate, pattern="^wall_"))

    # Error handler
    app.add_error_handler(error_handler)

    # Register commands in Telegram
    app.post_init = set_commands

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
