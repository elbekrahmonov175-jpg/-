from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_debts_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="? Äîáàâèòü äîëã")],
        [KeyboardButton(text="?? Ìîè äîëãè"), KeyboardButton(text="? Îòìåòèòü êàê îïëà÷åííûé")],
        [KeyboardButton(text="?? Ãëàâíîå ìåíþ")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_debt_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="?? ß äàë äåíüãè")],
        [KeyboardButton(text="?? ß âçÿë äåíüãè")],
        [KeyboardButton(text="? Îòìåíà")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_debts_inline_keyboard(debts: list, action: str = "pay") -> InlineKeyboardMarkup:
    """Ñîçäàíèå inline êëàâèàòóðû äëÿ ñïèñêà äîëãîâ"""
    keyboard = []
    for debt in debts:
        debt_id = debt['id']
        person = debt['person_name']
        amount = debt['amount']
        type_text = ">" if debt['type'] == 'i_gave' else "<"
        btn_text = f"{type_text} {person}: {amount}"
        callback_data = f"{action}_debt:{debt_id}"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=callback_data)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
