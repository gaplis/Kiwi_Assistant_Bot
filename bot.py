from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import TOKEN

from commands.start import start
from commands.profile import profile
from commands.not_found import not_found
from commands.change_city import change_city, cancel_change_city, ready_change_city
from commands.change_name import change_name, cancel_change_name, ready_change_name
from commands.diary import diary
from commands.add_task import add_task, cancel_add_task, get_task, get_deadline, incorrect_deadline

from classes_states.states import ChangeNameStates, ChangeCityStates, AddTaskStates
from classes_filters.filters import DateOrNoneFilter

bot = AsyncTeleBot(TOKEN, state_storage=StateMemoryStorage())


@bot.message_handler(commands=['start'])
async def start_command(message):
    await start(message, bot)


@bot.message_handler(commands=['profile'])
async def profile_command(message):
    await profile(message, bot)


@bot.message_handler(commands=['change_name'])
async def change_name_command(message):
    await change_name(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_name_command(message):
    await cancel_change_name(message, bot)


@bot.message_handler(state=ChangeNameStates.new_name)
async def ready_for_change_name(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_name_command(message)

    await ready_change_name(message, bot)


@bot.message_handler(commands=['change_city'])
async def change_city_command(message):
    await change_city(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_city_command(message):
    await cancel_change_city(message, bot)


@bot.message_handler(state=ChangeCityStates.new_city)
async def ready_for_change_city(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_city_command(message)

    await ready_change_city(message, bot)


@bot.message_handler(commands=['diary'])
async def diary_command(message):
    await diary(message, bot)


@bot.message_handler(commands=['add_task'])
async def add_task_command(message):
    await add_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_add_task_command(message):
    await cancel_add_task(message, bot)


@bot.message_handler(state=AddTaskStates.task)
async def ready_for_get_task(message):
    if message.text.lower() == 'отмена':
        return await cancel_add_task_command(message)

    await get_task(message, bot)


@bot.message_handler(state=AddTaskStates.deadline, is_date_or_none=True)
async def ready_for_get_deadline(message):
    await get_deadline(message, bot)


@bot.message_handler(state=AddTaskStates.deadline, is_date_or_none=False)
async def not_valid_deadline(message):
    await incorrect_deadline(message, bot)


@bot.message_handler(content_types=['text'])
async def insert_text(message):
    # ToDo: нужно изменить структуру проверки слов
    match message.text.lower():
        case 'профиль':
            await profile_command(message)
        case 'поменять имя':
            await change_name_command(message)
        case 'указать или изменить город':
            await change_city_command(message)
        case 'ежедневник':
            await diary_command(message)
        case 'добавить задачу':
            await add_task_command(message)
        case 'главное меню':
            await start_command(message)
        case _:
            await not_found_command(message)


@bot.message_handler()
async def not_found_command(message):
    await not_found(message, bot)
    await start_command(message)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(DateOrNoneFilter())
