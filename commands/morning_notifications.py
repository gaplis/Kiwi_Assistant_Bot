from telebot.async_telebot import AsyncTeleBot

from utils.db import DataBase
from utils.markups import main_menu_markup


async def on_morning_notifications(message, bot):
    db = DataBase()
    with db:
        db.update_user(message.from_user.id, db.NOTIFICATIONS, 1)

    on_text = f'Утренние уведомления включены!'

    await bot.send_message(message.chat.id, on_text, reply_markup=main_menu_markup())


async def off_morning_notifications(message, bot):
    db = DataBase()
    with db:
        db.update_user(message.from_user.id, db.NOTIFICATIONS, 0)

    off_text = f'Утренние уведомления выключены!'

    await bot.send_message(message.chat.id, off_text, reply_markup=main_menu_markup())


def route(bot: AsyncTeleBot):
    bot.register_message_handler(on_morning_notifications, on_morning_notifications_commands=True, pass_bot=True)
    bot.register_message_handler(off_morning_notifications, off_morning_notifications_commands=True, pass_bot=True)
