from aiogram import Router, types, F
from database import db
from keyboards.main_menu import get_main_menu

router = Router()  # ← ЭТО ВАЖНО!

@router.message(F.text == "💰 Баланс")
async def show_balance(message: types.Message):
    ...
