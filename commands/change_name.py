from telebot.async_telebot import types
from db import DataBase
from classes_states.states import ChangeNameStates


async def change_name(message, bot):
    change_text = 'Напиши новое имя'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    await bot.set_state(message.from_user.id, ChangeNameStates.new_name, message.chat.id)
    await bot.send_message(message.chat.id, change_text, parse_mode='html', reply_markup=markup)


async def cancel_change_name(message, bot):
    cancel_text = "Что-ж, тогда в другой раз. 😑"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, cancel_text, parse_mode='html', reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_change_name(message, bot):
    db = DataBase()
    with db as cursor:
        db.update_user(message.from_user.id, db.F_NAME, message.text)

        db.find_user(message.from_user.id, db.F_NAME)
        success_text = f'Отлично! Ваше новое имя - {cursor.fetchone()[0]}.'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, success_text, parse_mode="html", reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)
