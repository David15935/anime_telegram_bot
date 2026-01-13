import logging
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
)
from config.config import BOT_TOKEN
from bot.handlers import (
    start,
    help_cmd,
    anime_details,
    top_cmd,
    airing_cmd,
    wallpaper,
    inline_search,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Help"),
        BotCommand("anime", "Get anime details"),
        BotCommand("top", "Top anime"),
        BotCommand("airing", "Currently airing"),
        BotCommand("wallpaper", "Get wallpaper"),
    ])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("anime", anime_details))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("airing", airing_cmd))
    app.add_handler(CommandHandler("wallpaper", wallpaper))
    app.add_handler(InlineQueryHandler(inline_search))

    app.post_init = set_commands
    app.run_polling()

if __name__ == "__main__":
    main()
