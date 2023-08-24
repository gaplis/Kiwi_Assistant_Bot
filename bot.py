from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from config import TOKEN

from commands.start import start
from commands.profile import profile
from commands.change_name import change_name, cancel_change_name, ready_change_name

from states.states import ChangeNameStates

bot = AsyncTeleBot(TOKEN, state_storage=StateMemoryStorage())


@bot.message_handler(commands=['start'])
async def start_command(message):
    await start(message, bot)


@bot.message_handler(commands=['profile'])
async def profile_command(message):
    await profile(message, bot)


@bot.message_handler(commands=['change'])
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


@bot.message_handler(content_types=['text'])
async def insert_text(message):
    match message.text.lower():
        case 'профиль':
            await profile_command(message)
        case 'поменять имя':
            await change_name_command(message)
        case _:
            await start_command(message)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
