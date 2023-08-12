from aiogram.fsm.state import State, StatesGroup


class FactorialStates(StatesGroup):
    number = State()
