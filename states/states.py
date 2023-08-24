from telebot.asyncio_handler_backends import State, StatesGroup


class ChangeNameStates(StatesGroup):
    new_name = State()