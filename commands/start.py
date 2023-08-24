from telebot.async_telebot import types
from db import DataBase


async def start(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.all)
        if cursor.fetchone() is None:
            db.add_user(message.from_user.id, message.from_user.first_name,
                        message.from_user.username, message.from_user.language_code)
        else:
            db.update_user(message.from_user.id, db.u_name, message.from_user.username)

        db.find_user(message.from_user.id, db.f_name)
        start_text = f'<b>Привет, {cursor.fetchone()[0]}! Это Киви, я бот-ассистент. 😊</b>\n' \
                     f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton('Профиль')
    markup.row(profile_button)

    await bot.send_message(message.chat.id, start_text, parse_mode='html', reply_markup=markup)
