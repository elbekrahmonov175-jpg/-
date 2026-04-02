from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="➕ Добавить доход"), KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="📅 История"), KeyboardButton(text="🤝 Долги")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text="❌ Отмена")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
