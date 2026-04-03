from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_stats_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📥 Скачать Excel", callback_data="download_excel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
