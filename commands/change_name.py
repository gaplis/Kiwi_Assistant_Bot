from telebot.async_telebot import AsyncTeleBot

from utils.db import DataBase
from utils.states import ChangeNameStates
from utils.markups import cancel_markup, main_menu_markup


async def change_name(message, bot):
    change_text = 'Напиши новое имя'

    await bot.set_state(message.from_user.id, ChangeNameStates.new_name, message.chat.id)
    await bot.send_message(message.chat.id, change_text, reply_markup=cancel_markup())


async def cancel_change_name(message, bot):
    cancel_text = "Что-ж, тогда в другой раз. 😑"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_change_name(message, bot):
    db = DataBase()
    with db as cursor:
        db.update_user(message.from_user.id, db.F_NAME, message.text)

        db.find_user(message.from_user.id, db.F_NAME)
        new_name = cursor.fetchone()[0]
    success_text = f'Отлично! Ваше новое имя - {new_name}.'

    await bot.send_message(message.chat.id, success_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


def route(bot: AsyncTeleBot):
    bot.register_message_handler(change_name, change_name_commands=True, pass_bot=True)
    bot.register_message_handler(cancel_change_name, state=ChangeNameStates.new_name, cancel_commands=True,
                                 pass_bot=True)
    bot.register_message_handler(ready_change_name, state=ChangeNameStates.new_name, pass_bot=True)
