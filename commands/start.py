from utils.db import DataBase
from utils.markups import start_markup


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
        name = cursor.fetchone()[0]

    if message.text == '/start':
        start_text = f'<b>Привет, {name}! Это Киви, я бот-ассистент. 😊</b>\n' \
                     f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '
    else:
        start_text = f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '

    await bot.send_message(message.chat.id, start_text, parse_mode='html', reply_markup=start_markup())
