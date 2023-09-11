from telebot.async_telebot import types
from db import DataBase


async def start(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        if cursor.fetchone() is None:
            db.add_user(message.from_user.id, message.from_user.first_name,
                        message.from_user.username, message.from_user.language_code)
        else:
            db.update_user(message.from_user.id, db.U_NAME, message.from_user.username)

        db.find_user(message.from_user.id, db.F_NAME)
        if message.text == '/start':
            start_text = f'<b>Привет, {cursor.fetchone()[0]}! Это Киви, я бот-ассистент. 😊</b>\n' \
                         f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '
        else:
            start_text = f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton('Профиль')
    diary_button = types.KeyboardButton('Ежедневник')
    whether_button = types.KeyboardButton('Погода')
    search_button = types.KeyboardButton('Поиск')
    games_button = types.KeyboardButton('Игры')
    help_button = types.KeyboardButton('Помощь')
    markup.row(profile_button)
    markup.row(diary_button)
    markup.row(whether_button)
    markup.row(search_button)
    markup.row(games_button)
    markup.row(help_button)

    await bot.send_message(message.chat.id, start_text, parse_mode='html', reply_markup=markup)
