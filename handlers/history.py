from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(F.text == "?? Èñòîðèÿ")
async def show_history(message: types.Message):
    history = await db.get_history(message.from_user.id, limit=10)
    
    if not history:
        await message.answer(
            "?? Èñòîðèÿ îïåðàöèé ïóñòà",
            reply_markup=get_main_menu()
        )
        return
    
    text = "?? <b>Ïîñëåäíèå 10 îïåðàöèé:</b>\n\n"
    
    for item in history:
        category = item['category']
        amount = item['amount']
        date = item['date'][:10]  # Òîëüêî äàòà áåç âðåìåíè
        
        if item['type'] == 'income':
            text += f"?? <b>{category}</b> +{amount:,} ñóì ({date})\n"
        else:
            text += f"?? <b>{category}</b> -{amount:,} ñóì ({date})\n"
    
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
