from telebot.asyncio_handler_backends import State, StatesGroup


class ChangeNameStates(StatesGroup):
    new_name = State()


class ChangeCityStates(StatesGroup):
    new_city = State()


class AddTaskStates(StatesGroup):
    task = State()
    deadline = State()


class ChangeTaskStates(StatesGroup):
    id_task = State()
    new_data = State()


class DeleteTaskStates(StatesGroup):
    id_task = State()
