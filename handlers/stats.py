from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    
    today_expenses = await db.get_today_expenses(user_id)
    month_expenses = await db.get_month_expenses(user_id)
    top_category = await db.get_top_category(user_id)
    
    text = "📊 <b>Статистика расходов</b>\n\n"
    text += f"📅 <b>Сегодня:</b> {today_expenses:,} сум\n"
    text += f"📆 <b>Текущий месяц:</b> {month_expenses:,} сум\n\n"
    
    if top_category:
        text += f"🏆 <b>Самая частая категория:</b> {top_category}"
    else:
        text += "🏆 Пока нет данных о расходах"
    
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
