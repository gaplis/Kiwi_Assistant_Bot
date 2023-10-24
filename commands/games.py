from telebot.async_telebot import AsyncTeleBot

from utils.markups import games_markup


async def games(message, bot):
    games_text = f'Во что хочешь поиграть?'

    await bot.send_message(message.chat.id, games_text, reply_markup=games_markup())


def route(bot: AsyncTeleBot):
    bot.register_message_handler(games, games_commands=True, pass_bot=True)
