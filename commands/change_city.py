from telebot.async_telebot import AsyncTeleBot

from utils.db import DataBase
from utils.states import ChangeCityStates
from utils.markups import cancel_markup, main_menu_markup
from utils.timezones import get_timezone
from config import OPEN_WEATHER_TOKEN


async def change_city(message, bot):
    change_text = 'Напиши свой город'

    await bot.set_state(message.from_user.id, ChangeCityStates.new_city, message.chat.id)
    await bot.send_message(message.chat.id, change_text, reply_markup=cancel_markup())


async def cancel_change_city(message, bot):
    cancel_text = "Если ты не укажешь нужный город, то не сможешь получать актуальные данные о погоде.\n" \
                  "Ты в любой момент можешь снова отправить мне форму для смены города, если нужно будет. 😉"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_change_city(message, bot):
    db = DataBase()
    with db as cursor:
        db.update_user(message.from_user.id, db.U_CITY, message.text.title())
        timezone = get_timezone(message.text, OPEN_WEATHER_TOKEN)
        if timezone:
            db.update_user(message.from_user.id, db.TIMEZONE, timezone)

        db.find_user(message.from_user.id, db.U_CITY)
        new_city = cursor.fetchone()[0]
    success_text = f'Отлично! Указанный город - {new_city}.'

    await bot.send_message(message.chat.id, success_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


def route(bot: AsyncTeleBot):
    bot.register_message_handler(change_city, change_city_commands=True, pass_bot=True)
    bot.register_message_handler(cancel_change_city, state=ChangeCityStates.new_city, cancel_commands=True,
                                 pass_bot=True)
    bot.register_message_handler(ready_change_city, state=ChangeCityStates.new_city, pass_bot=True)
