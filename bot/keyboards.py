from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def anime_buttons(trailer, mal, anilist):
    buttons = [
        [
            InlineKeyboardButton("🎬 Trailer", url=trailer),
            InlineKeyboardButton("📘 MAL", url=mal),
        ],
        [
            InlineKeyboardButton("⭐ AniList", url=anilist)
        ]
    ]
    return InlineKeyboardMarkup(buttons)
