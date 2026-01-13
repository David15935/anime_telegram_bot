import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)

from config.config import BOT_TOKEN
from bot.handlers import (
    start,
    anime_details,
    top_anime,
    airing_anime,
    wallpaper,
    inline_search,
    paginate,
)

# ---------- LOGGING ----------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.exception("Unhandled exception", exc_info=context.error)


def main():
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime_details))
    app.add_handler(CommandHandler("top", top_anime))
    app.add_handler(CommandHandler("airing", airing_anime))
    app.add_handler(CommandHandler("wallpaper", wallpaper))

    app.add_handler(InlineQueryHandler(inline_search))
    app.add_handler(CallbackQueryHandler(paginate))

    app.add_error_handler(error_handler)

    logger.info("Bot running.")
    app.run_polling()


if __name__ == "__main__":
    main()
