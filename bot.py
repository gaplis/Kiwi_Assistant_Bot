from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import TOKEN

from router import router
from utils.filters import register_filters
from utils.commands_filters import register_commands_filters

bot = AsyncTeleBot(TOKEN, state_storage=StateMemoryStorage(), parse_mode='html')

router(bot)

register_filters(bot)
register_commands_filters(bot)
