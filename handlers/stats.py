import os
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from openpyxl import Workbook
from database import db
from keyboards.main_menu import get_main_menu
from keyboards.stats import get_stats_keyboard

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
    
    await message.answer(text, reply_markup=get_stats_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "download_excel")
async def download_excel(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # Получаем все транзакции
    transactions = await db.get_all_transactions(user_id)
    
    if not transactions:
        await callback.answer("Нет данных для отчёта", show_alert=True)
        return
    
    # Создаём Excel файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Финансы"
    
    # Заголовки
    ws.append(["Дата", "Тип", "Категория", "Сумма"])
    
    # Данные
    for t in transactions:
        type_name = "Доход" if t["type"] == "income" else "Расход"
        date = t["date"][:10]  # Только дата
        ws.append([date, type_name, t["category"], t["amount"]])
    
    # Сохраняем
    filename = f"finance_report_{user_id}.xlsx"
    wb.save(filename)
    
    # Отправляем файл
    file = FSInputFile(filename)
    await callback.message.answer_document(
        file, 
        caption="📊 Ваш финансовый отчёт",
        reply_markup=get_main_menu()
    )
    
    # Удаляем временный файл
    os.remove(filename)
    await callback.answer()
