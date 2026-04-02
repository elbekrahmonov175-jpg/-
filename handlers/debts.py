from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.finance_states import DebtState, DebtPayState
from keyboards.debts import get_debts_menu, get_debt_type_keyboard, get_debts_inline_keyboard
from keyboards.main_menu import get_main_menu, get_cancel_keyboard
from database import db

router = Router()


@router.message(F.text == "?? Äîëãè")
async def debts_menu(message: types.Message):
    await message.answer(
        "?? <b>Óïðàâëåíèå äîëãàìè</b>\n\n"
        "Âûáåðè äåéñòâèå:",
        reply_markup=get_debts_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "? Äîáàâèòü äîëã")
async def start_add_debt(message: types.Message, state: FSMContext):
    await state.set_state(DebtState.type_)
    await message.answer(
        "Êòî êîìó äîëæåí?",
        reply_markup=get_debt_type_keyboard()
    )


@router.message(DebtState.type_)
async def process_debt_type(message: types.Message, state: FSMContext):
    if message.text == "? Îòìåíà":
        await state.clear()
        await message.answer("Äåéñòâèå îòìåíåíî", reply_markup=get_debts_menu())
        return
    
    if message.text == "?? ß äàë äåíüãè":
        await state.update_data(type_="i_gave")
    elif message.text == "?? ß âçÿë äåíüãè":
        await state.update_data(type_="i_took")
    else:
        await message.answer("Ïîæàëóéñòà, âûáåðè âàðèàíò èç êíîïîê")
        return
    
    await state.set_state(DebtState.person_name)
    await message.answer(
        "Ââåäè èìÿ ÷åëîâåêà:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(DebtState.person_name)
async def process_debt_person(message: types.Message, state: FSMContext):
    if message.text == "? Îòìåíà":
        await state.clear()
        await message.answer("Äåéñòâèå îòìåíåíî", reply_markup=get_debts_menu())
        return
    
    name = message.text.strip()
    if len(name) < 1 or len(name) > 50:
        await message.answer("Èìÿ äîëæíî áûòü îò 1 äî 50 ñèìâîëîâ")
        return
    
    await state.update_data(person_name=name)
    await state.set_state(DebtState.amount)
    await message.answer(
        "Ââåäè ñóììó äîëãà (òîëüêî ÷èñëî):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(DebtState.amount)
async def process_debt_amount(message: types.Message, state: FSMContext):
    if message.text == "? Îòìåíà":
        await state.clear()
        await message.answer("Äåéñòâèå îòìåíåíî", reply_markup=get_debts_menu())
        return
    
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            await message.answer("Ñóììà äîëæíà áûòü áîëüøå 0")
            return
    except ValueError:
        await message.answer("Ââåäè òîëüêî ÷èñëî:")
        return
    
    data = await state.get_data()
    type_ = data['type_']
    person_name = data['person_name']
    
    # Ñîõðàíÿåì äîëã
    await db.add_debt(
        user_id=message.from_user.id,
        person_name=person_name,
        amount=amount,
        type_=type_
    )
    
    type_text = "äàë" if type_ == "i_gave" else "âçÿë"
    await state.clear()
    await message.answer(
        f"? Äîëã çàïèñàí!\n\n"
        f"Òû {type_text} {person_name}: {amount:,} ñóì",
        reply_markup=get_debts_menu()
    )


@router.message(F.text == "?? Ìîè äîëãè")
async def show_debts(message: types.Message):
    debts = await db.get_debts(message.from_user.id, is_paid=False)
    
    if not debts:
        await message.answer(
            "?? Ó òåáÿ íåò àêòèâíûõ äîëãîâ!",
            reply_markup=get_debts_menu()
        )
        return
    
    text = "?? <b>Òâîè äîëãè:</b>\n\n"
    
    for debt in debts:
        person = debt['person_name']
        amount = debt['amount']
        date = debt['date'][:10]
        
        if debt['type'] == 'i_gave':
            text += f"?? Òû äàë <b>{person}</b>: {amount:,} ñóì ({date})\n"
        else:
            text += f"?? Òû âçÿë ó <b>{person}</b>: {amount:,} ñóì ({date})\n"
    
    text += "\n<i>Äëÿ îòìåòêè äîëãà êàê îïëà÷åííîãî èñïîëüçóé êíîïêó '? Îòìåòèòü êàê îïëà÷åííûé'</i>"
    
    await message.answer(text, reply_markup=get_debts_menu(), parse_mode="HTML")


@router.message(F.text == "? Îòìåòèòü êàê îïëà÷åííûé")
async def start_pay_debt(message: types.Message, state: FSMContext):
    debts = await db.get_debts(message.from_user.id, is_paid=False)
    
    if not debts:
        await message.answer(
            "?? Íåò äîëãîâ äëÿ îòìåòêè",
            reply_markup=get_debts_menu()
        )
        return
    
    await state.set_state(DebtPayState.selecting)
    await message.answer(
        "Âûáåðè äîëã äëÿ îòìåòêè êàê îïëà÷åííûé:",
        reply_markup=get_debts_inline_keyboard(debts, action="pay")
    )


@router.callback_query(DebtPayState.selecting, F.data.startswith("pay_debt:"))
async def process_pay_debt(callback: CallbackQuery, state: FSMContext):
    debt_id = int(callback.data.split(":")[1])
    
    success = await db.mark_debt_paid(debt_id, callback.from_user.id)
    
    if success:
        await callback.message.edit_text("? Äîëã îòìå÷åí êàê îïëà÷åííûé!")
    else:
        await callback.message.edit_text("? Îøèáêà: äîëã íå íàéäåí")
    
    await state.clear()
    await callback.answer()
