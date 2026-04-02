from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import ExpenseState
from keyboards.categories import get_expense_categories
from keyboards.main_menu import get_main_menu, get_cancel_keyboard
from database import db

router = Router()  # ← ЭТО ВАЖНО!

@router.message(F.text == "➖ Добавить расход")
async def start_expense(message: types.Message, state: FSMContext):
    ...
