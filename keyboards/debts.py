from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_debts_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="➕ Добавить долг")],
        [KeyboardButton(text="📋 Мои долги"), KeyboardButton(text="✅ Отметить как оплаченный")],
        [KeyboardButton(text="🔙 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_debt_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="💸 Я дал деньги")],
        [KeyboardButton(text="💰 Я взял деньги")],
        [KeyboardButton(text="❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_debts_inline_keyboard(debts: list, action: str = "pay") -> InlineKeyboardMarkup:
    keyboard = []
    for debt in debts:
        debt_id = debt['id']
        person = debt['person_name']
        amount = debt['amount']
        type_text = "→" if debt['type'] == 'i_gave' else "←"
        btn_text = f"{type_text} {person}: {amount}"
        callback_data = f"{action}_debt:{debt_id}"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=callback_data)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
