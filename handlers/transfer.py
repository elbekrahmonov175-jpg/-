from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import TransferState
from keyboards.main_menu import get_main_menu, get_cancel_keyboard, get_transfer_direction_keyboard
from database import db

router = Router()

TRANSFER_DIRECTIONS = ("🏧 Снять наличные", "💳 С наличных на карту")


@router.message(F.text == "💳 Перевод / Снятие")
async def start_transfer(message: types.Message, state: FSMContext):
    await state.set_state(TransferState.direction)
    await message.answer(
        "Что хочешь сделать?",
        reply_markup=get_transfer_direction_keyboard()
    )


@router.message(TransferState.direction)
async def process_transfer_direction(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    if message.text not in TRANSFER_DIRECTIONS:
        await message.answer("Пожалуйста, выбери действие из кнопок:")
        return

    await state.update_data(direction=message.text)
    await state.set_state(TransferState.amount)
    await message.answer(
        "Введи сумму (только число):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(TransferState.amount)
async def process_transfer_amount(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    try:
        amount = int(message.text.strip())
        if amount <= 0:
            await message.answer("Сумма должна быть больше 0. Попробуй снова:")
            return
    except ValueError:
        await message.answer("Пожалуйста, введи только число без пробелов и букв:")
        return

    await state.update_data(amount=amount)
    await state.set_state(TransferState.commission)
    await message.answer(
        "Была ли комиссия? Если да — введи сумму комиссии.\nЕсли нет — введи 0:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(TransferState.commission)
async def process_transfer_commission(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    try:
        commission = int(message.text.strip())
        if commission < 0:
            await message.answer("Комиссия не может быть отрицательной. Введи 0 если комиссии нет:")
            return
    except ValueError:
        await message.answer("Пожалуйста, введи только число (0 если комиссии нет):")
        return

    data = await state.get_data()
    direction = data['direction']
    amount = data['amount']
    total = amount + commission

    # Сохраняем как расход: сама сумма перевода
    await db.add_transaction(
        user_id=message.from_user.id,
        type_="expense",
        category=direction,
        amount=amount
    )

    # Если есть комиссия — отдельной строкой
    if commission > 0:
        await db.add_transaction(
            user_id=message.from_user.id,
            type_="expense",
            category=f"Комиссия ({direction})",
            amount=commission
        )

    await state.clear()

    commission_text = f"\nКомиссия: -{commission:,} сум" if commission > 0 else "\nКомиссия: нет"
    await message.answer(
        f"✅ Операция записана!\n\n"
        f"Тип: {direction}\n"
        f"Сумма: -{amount:,} сум"
        f"{commission_text}\n"
        f"Итого списано: -{total:,} сум",
        reply_markup=get_main_menu()
    )
