from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu

router = Router()  # ← ЭТО ВАЖНО!

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой личный финансовый менеджер...",
        reply_markup=get_main_menu()
    )

@router.message(F.text == "🔙 Главное меню")
async def back_to_main(message: types.Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu())
