from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="➕ Добавить доход"), KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="📅 История"), KeyboardButton(text="🤝 Долги")],
        [KeyboardButton(text="💳 Перевод / Снятие")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text="❌ Отмена")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_payment_method_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="💳 На карту"), KeyboardButton(text="💵 Наличные")],
        [KeyboardButton(text="❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_transfer_direction_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🏧 Снять наличные")],
        [KeyboardButton(text="💳 С наличных на карту")],
        [KeyboardButton(text="❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
