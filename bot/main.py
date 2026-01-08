import logging
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from config.config import BOT_TOKEN
from bot.handlers import inline_search, anime_details, paginate


# ---------- LOGGING CONFIG ----------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ---------- ERROR HANDLER ----------
async def error_handler(update, context):
    logger.exception(
        "Unhandled exception while handling an update",
        exc_info=context.error,
    )


# ---------- MAIN ----------
def main():
    logger.info("Starting bot...")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    logger.info("Bot initialized, registering handlers...")

    app.add_handler(CommandHandler("anime", anime_details))
    app.add_handler(CallbackQueryHandler(paginate, pattern="^page:"))

    # 🔥 THIS WAS MISSING
    app.add_error_handler(error_handler)

    logger.info("Connecting to Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()

