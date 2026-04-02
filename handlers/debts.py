from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.finance_states import DebtState, DebtPayState
from keyboards.debts import get_debts_menu, get_debt_type_keyboard, get_debts_inline_keyboard
from keyboards.main_menu import get_main_menu, get_cancel_keyboard
from database import db

router = Router()  # ← ЭТО ВАЖНО!

@router.message(F.text == "🤝 Долги")
async def debts_menu(message: types.Message):
    ...
