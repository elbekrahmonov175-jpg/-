from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "?? Áàëàíñ")
async def show_balance(message: types.Message):
    balance_data = await db.get_balance(message.from_user.id)
    
    balance = balance_data['balance']
    income = balance_data['income']
    expense = balance_data['expense']
    
    # Îïğåäåëÿåì ıìîäçè äëÿ áàëàíñà
    balance_emoji = "??" if balance >= 0 else "??"
    
    text = (
        f"{balance_emoji} <b>Áàëàíñ: {balance:,} ñóì</b>\n\n"
        f"?? Îáùèé äîõîä: {income:,} ñóì\n"
        f"?? Îáùèé ğàñõîä: {expense:,} ñóì"
    )
    
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
