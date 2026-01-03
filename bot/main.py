import logging
from telegram.ext import Application, CommandHandler
from telegram.request import HTTPXRequest

from config.config import BOT_TOKEN
from bot.handlers import start, anime, top, airing, wallpaper

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------------- ERROR HANDLER ----------------
async def error_handler(update, context):
    print("⚠️ Error:", context.error)

# ---------------- MAIN ----------------
def main():
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("airing", airing))
    app.add_handler(CommandHandler("wallpaper", wallpaper))

    # Error handler
    app.add_error_handler(error_handler)

    print("Anime Bot running...")
    app.run_polling()

# ---------------- ENTRY ----------------
if __name__ == "__main__":
    main()
