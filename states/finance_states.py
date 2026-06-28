from aiogram.fsm.state import State, StatesGroup


class IncomeState(StatesGroup):
    category = State()
    amount = State()


class ExpenseState(StatesGroup):
    category = State()
    custom_category = State()   # для "Другое" — что именно куплено
    amount = State()
    payment_method = State()    # карта или наличные


class DebtState(StatesGroup):
    type_ = State()  # i_gave или i_took
    person_name = State()
    amount = State()


class DebtPayState(StatesGroup):
    selecting = State()


class TransferState(StatesGroup):
    direction = State()     # снять наличные / с наличных на карту
    amount = State()
    commission = State()    # сумма комиссии
