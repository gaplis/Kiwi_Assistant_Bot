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
from commands.change_task import change_task, cancel_change_task, get_task_id, incorrect_task_id, get_new_data
from commands.delete_task import delete_task, cancel_delete_task, ready_delete_task, incorrect_del_task_id
from commands.weather_now import weather_now
from commands.weather_5_days import weather_5_days

from utils.states import ChangeNameStates, ChangeCityStates, AddTaskStates, ChangeTaskStates, DeleteTaskStates
from utils.filters import DateOrNoneFilter, IsValidIDFilter
from utils.commands_lists import PROFILE, CHANGE_NAME, CHANGE_CITY, DIARY, ADD_TASK, CHANGE_TASK, DELETE_TASK, \
    MAIN_MENU, WEATHER_NOW, WEATHER_5_DAYS

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
    if message.text.lower() == 'отмена':
        return await cancel_add_task_command(message)

    await get_deadline(message, bot)


@bot.message_handler(state=AddTaskStates.deadline, is_date_or_none=False)
async def not_valid_deadline(message):
    await incorrect_deadline(message, bot)


@bot.message_handler(commands=['change_task'])
async def change_task_command(message):
    await change_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_task_command(message):
    await cancel_change_task(message, bot)


@bot.message_handler(state=ChangeTaskStates.id_task, is_valid_id=True)
async def ready_for_get_task_id(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_task_command(message)

    await get_task_id(message, bot)


@bot.message_handler(state=ChangeTaskStates.id_task, is_valid_id=False)
async def not_valid_task_id(message):
    await incorrect_task_id(message, bot)


@bot.message_handler(state=ChangeTaskStates.new_data)
async def ready_for_get_new_data(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_task_command(message)

    await get_new_data(message, bot)


@bot.message_handler(commands=['delete_task'])
async def delete_task_command(message):
    await delete_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_delete_task_command(message):
    await cancel_delete_task(message, bot)


@bot.message_handler(state=DeleteTaskStates.id_task, is_valid_id=True)
async def ready_for_delete_task(message):
    if message.text.lower() == 'отмена':
        return await cancel_delete_task_command(message)

    await ready_delete_task(message, bot)


@bot.message_handler(state=DeleteTaskStates.id_task, is_valid_id=False)
async def not_valid_del_task_id(message):
    await incorrect_del_task_id(message, bot)


@bot.message_handler(commands=['weather_now'])
async def weather_now_command(message):
    await weather_now(message, bot)


@bot.message_handler(commands=['weather_5_days'])
async def weather_5_days_command(message):
    await weather_5_days(message, bot)


@bot.message_handler(content_types=['text'])
async def insert_text(message):
    command = message.text.lower()
    if command in PROFILE:
        await profile_command(message)
    elif command in CHANGE_NAME:
        await change_name_command(message)
    elif command in CHANGE_CITY:
        await change_city_command(message)
    elif command in DIARY:
        await diary_command(message)
    elif command in ADD_TASK:
        await add_task_command(message)
    elif command in CHANGE_TASK:
        await change_task_command(message)
    elif command in DELETE_TASK:
        await delete_task_command(message)
    elif command in MAIN_MENU:
        await start_command(message)
    elif command in WEATHER_5_DAYS:
        await weather_5_days_command(message)
    elif command in WEATHER_NOW or ('погода' in command and len(command.split()) > 1):
        await weather_now_command(message)
    else:
        await not_found_command(message)


@bot.message_handler()
async def not_found_command(message):
    await not_found(message, bot)
    await start_command(message)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(DateOrNoneFilter())
bot.add_custom_filter(IsValidIDFilter())
