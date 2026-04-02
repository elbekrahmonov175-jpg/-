from aiogram.fsm.state import State, StatesGroup


class IncomeState(StatesGroup):
    category = State()
    amount = State()


class ExpenseState(StatesGroup):
    category = State()
    amount = State()


class DebtState(StatesGroup):
    type_ = State()  # i_gave čëč i_took
    person_name = State()
    amount = State()


class DebtPayState(StatesGroup):
    selecting = State()
