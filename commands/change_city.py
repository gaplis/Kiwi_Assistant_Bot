from telebot.async_telebot import types
from db import DataBase
from classes_states.states import ChangeCityStates


async def change_city(message, bot):
    change_text = 'Напиши свой город'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    await bot.set_state(message.from_user.id, ChangeCityStates.new_city, message.chat.id)
    await bot.send_message(message.chat.id, change_text, parse_mode='html', reply_markup=markup)


async def cancel_change_city(message, bot):
    cancel_text = "Если ты не укажешь нужный город, то не сможешь получать актуальные данные о погоде.\n" \
                  "Ты в любой момент можешь снова отправить мне форму для смены города, если нужно будет. 😉"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, cancel_text, parse_mode='html', reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_change_city(message, bot):
    db = DataBase()
    with db as cursor:
        db.update_user(message.from_user.id, db.u_city, message.text)

        db.find_user(message.from_user.id, db.u_city)
        success_text = f'Отлично! Указанный город - {cursor.fetchone()[0]}.'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, success_text, parse_mode="html", reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)

