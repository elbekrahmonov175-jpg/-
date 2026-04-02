from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "📅 История")
async def show_history(message: types.Message):
    history = await db.get_history(message.from_user.id, limit=10)
    
    if not history:
        await message.answer(
            "📭 История операций пуста",
            reply_markup=get_main_menu()
        )
        return
    
    text = "📅 <b>Последние 10 операций:</b>\n\n"
    
    for item in history:
        category = item['category']
        amount = item['amount']
        date = item['date'][:10]
        
        if item['type'] == 'income':
            text += f"📥 <b>{category}</b> +{amount:,} сум ({date})\n"
        else:
            text += f"📤 <b>{category}</b> -{amount:,} сум ({date})\n"
    
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
