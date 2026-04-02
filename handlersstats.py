from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "?? Ñòàòèñòèêà")
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    
    # Ïîëó÷àåì ñòàòèñòèêó
    today_expenses = await db.get_today_expenses(user_id)
    month_expenses = await db.get_month_expenses(user_id)
    top_category = await db.get_top_category(user_id)
    
    text = "?? <b>Ñòàòèñòèêà ðàñõîäîâ</b>\n\n"
    text += f"?? <b>Ñåãîäíÿ:</b> {today_expenses:,} ñóì\n"
    text += f"?? <b>Òåêóùèé ìåñÿö:</b> {month_expenses:,} ñóì\n\n"
    
    if top_category:
        text += f"?? <b>Ñàìàÿ ÷àñòàÿ êàòåãîðèÿ:</b> {top_category}"
    else:
        text += "?? Ïîêà íåò äàííûõ î ðàñõîäàõ"
    
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
