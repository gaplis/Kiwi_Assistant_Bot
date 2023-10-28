from telebot.async_telebot import AsyncTeleBot

from utils.search import get_search_data
from utils.states import SearchState
from utils.markups import cancel_markup, main_menu_markup, more_search_markup, data_search_inline_markup


async def search_in_google(message, bot):
    search_text = 'Что хочешь найти?'

    await bot.set_state(message.from_user.id, SearchState.search_data, message.chat.id)
    await bot.send_message(message.chat.id, search_text, reply_markup=cancel_markup())


async def cancel_search_in_google(message, bot):
    cancel_text = "Возращайся 😉\n"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_search_in_google(message, bot):
    await bot.delete_state(message.from_user.id, message.chat.id)

    search_data = await get_search_data(message.text)

    success_text = f"Вот что найдено по твоему запросу:\n\n"
    for i, item in enumerate(search_data, start=1):
        if i != len(search_data):
            success_text += f'{i}: {item["text"]}\n\n'
        else:
            success_text += f'Больше информации ты можешь найти по ссылкам снизу\n'

    more_search_text = 'Может, хочешь найти что-то ещё?'

    await bot.send_message(message.chat.id, success_text, reply_markup=data_search_inline_markup(search_data))
    await bot.send_message(message.chat.id, more_search_text, reply_markup=more_search_markup())


def route(bot: AsyncTeleBot):
    bot.register_message_handler(search_in_google, search_commands=True, pass_bot=True)
    bot.register_message_handler(cancel_search_in_google, state=SearchState.search_data, cancel_commands=True,
                                 pass_bot=True)
    bot.register_message_handler(ready_search_in_google, state=SearchState.search_data, pass_bot=True)
