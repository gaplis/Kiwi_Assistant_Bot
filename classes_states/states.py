from telebot.asyncio_handler_backends import State, StatesGroup


class ChangeNameStates(StatesGroup):
    new_name = State()


class ChangeCityStates(StatesGroup):
    new_city = State()
