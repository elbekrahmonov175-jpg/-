from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import IncomeState
from keyboards.categories import get_income_categories
from keyboards.main_menu import get_main_menu, get_cancel_keyboard
from database import db

router = Router()  # ← ЭТО ВАЖНО!

@router.message(F.text == "➕ Добавить доход")
async def start_income(message: types.Message, state: FSMContext):
    ...
