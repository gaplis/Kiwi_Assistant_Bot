from telebot.async_telebot import AsyncTeleBot

from commands.main_menu import main_menu


async def not_found(message, bot):
    not_found_text = f'<i>Пока что не знаю, что делать с этой информацией...\n</i>'

    await bot.send_message(message.chat.id, not_found_text)
    await main_menu(message, bot)


def route(bot: AsyncTeleBot):
    bot.register_message_handler(not_found, pass_bot=True)
