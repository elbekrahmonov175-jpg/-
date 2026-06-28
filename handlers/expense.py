from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.finance_states import ExpenseState
from keyboards.categories import get_expense_categories
from keyboards.main_menu import get_main_menu, get_cancel_keyboard, get_payment_method_keyboard
from database import db

router = Router()


@router.message(F.text == "➖ Добавить расход")
async def start_expense(message: types.Message, state: FSMContext):
    await state.set_state(ExpenseState.category)
    await message.answer(
        "Выбери категорию расхода:",
        reply_markup=get_expense_categories()
    )


@router.message(ExpenseState.category)
async def process_expense_category(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    from config import EXPENSE_CATEGORIES
    if message.text not in EXPENSE_CATEGORIES:
        await message.answer("Пожалуйста, выбери категорию из списка")
        return

    await state.update_data(category=message.text)

    # Если выбрано "Другое" — спрашиваем что именно
    if message.text == "Другое":
        await state.set_state(ExpenseState.custom_category)
        await message.answer(
            "Напиши, что именно ты купил/оплатил:",
            reply_markup=get_cancel_keyboard()
        )
    else:
        await state.set_state(ExpenseState.amount)
        await message.answer(
            "Введи сумму расхода (только число):",
            reply_markup=get_cancel_keyboard()
        )


@router.message(ExpenseState.custom_category)
async def process_expense_custom_category(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    if not message.text or len(message.text.strip()) == 0:
        await message.answer("Пожалуйста, напиши название:")
        return

    # Сохраняем уточнение как часть категории
    await state.update_data(category=f"Другое ({message.text.strip()})")
    await state.set_state(ExpenseState.amount)
    await message.answer(
        "Введи сумму расхода (только число):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(ExpenseState.amount)
async def process_expense_amount(message: types.Message, state: FSMContext):
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
    await state.set_state(ExpenseState.payment_method)
    await message.answer(
        "Куда списываем расход?",
        reply_markup=get_payment_method_keyboard()
    )


@router.message(ExpenseState.payment_method)
async def process_expense_payment_method(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=get_main_menu())
        return

    if message.text not in ("💳 На карту", "💵 Наличные"):
        await message.answer("Пожалуйста, выбери способ оплаты из кнопок ниже:")
        return

    data = await state.get_data()
    category = data['category']
    amount = data['amount']
    payment = message.text

    await db.add_transaction(
        user_id=message.from_user.id,
        type_="expense",
        category=category,
        amount=amount
    )

    await state.clear()
    await message.answer(
        f"✅ Расход добавлен!\n\n"
        f"Категория: {category}\n"
        f"Сумма: -{amount:,} сум\n"
        f"Способ: {payment}",
        reply_markup=get_main_menu()
    )
