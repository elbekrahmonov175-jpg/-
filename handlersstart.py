from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "?? Ïðèâåò! ß òâîé ëè÷íûé ôèíàíñîâûé ìåíåäæåð.\n\n"
        "ß ïîìîãó òåáå:\n"
        "• ?? Îòñëåæèâàòü äîõîäû è ðàñõîäû\n"
        "• ?? Àíàëèçèðîâàòü ôèíàíñû\n"
        "• ?? Ó÷èòûâàòü äîëãè\n\n"
        "Âûáåðè äåéñòâèå â ìåíþ íèæå:",
        reply_markup=get_main_menu()
    )


@router.message(F.text == "?? Ãëàâíîå ìåíþ")
async def back_to_main(message: types.Message):
    await message.answer("Ãëàâíîå ìåíþ:", reply_markup=get_main_menu())
