from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import ExpenseState
from keyboards.categories import get_expense_categories
from keyboards.main_menu import get_main_menu, get_cancel_keyboard
from database import db

router = Router()


@router.message(F.text == "? Äîáàâèòü ðàñõîä")
async def start_expense(message: types.Message, state: FSMContext):
    await state.set_state(ExpenseState.category)
    await message.answer(
        "Âûáåðè êàòåãîðèþ ðàñõîäà:",
        reply_markup=get_expense_categories()
    )


@router.message(ExpenseState.category)
async def process_expense_category(message: types.Message, state: FSMContext):
    if message.text == "? Îòìåíà":
        await state.clear()
        await message.answer("Äåéñòâèå îòìåíåíî", reply_markup=get_main_menu())
        return
    
    from config import EXPENSE_CATEGORIES
    if message.text not in EXPENSE_CATEGORIES:
        await message.answer("Ïîæàëóéñòà, âûáåðè êàòåãîðèþ èç ñïèñêà")
        return
    
    await state.update_data(category=message.text)
    await state.set_state(ExpenseState.amount)
    await message.answer(
        "Ââåäè ñóììó ðàñõîäà (òîëüêî ÷èñëî):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ExpenseState.amount)
async def process_expense_amount(message: types.Message, state: FSMContext):
    if message.text == "? Îòìåíà":
        await state.clear()
        await message.answer("Äåéñòâèå îòìåíåíî", reply_markup=get_main_menu())
        return
    
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            await message.answer("Ñóììà äîëæíà áûòü áîëüøå 0. Ïîïðîáóé ñíîâà:")
            return
    except ValueError:
        await message.answer("Ïîæàëóéñòà, ââåäè òîëüêî ÷èñëî áåç ïðîáåëîâ è áóêâ:")
        return
    
    data = await state.get_data()
    category = data['category']
    
    # Ñîõðàíÿåì â áàçó
    await db.add_transaction(
        user_id=message.from_user.id,
        type_="expense",
        category=category,
        amount=amount
    )
    
    await state.clear()
    await message.answer(
        f"? Ðàñõîä äîáàâëåí!\n\n"
        f"Êàòåãîðèÿ: {category}\n"
        f"Ñóììà: -{amount:,} ñóì",
        reply_markup=get_main_menu()
    )
