from telebot.async_telebot import types
from utils.db import DataBase


async def profile(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        data = cursor.fetchone()
        profile_text = f'<b>Твой профиль</b>\n' \
                       f'<i>Имя: </i>{data[2]}\n' \
                       f'<i>Никнейм: </i>@{data[3]}\n' \
                       f'<i>id: </i>{data[0]}\n' \
                       f'<i>TGid: </i>{data[1]}\n' \
                       f'<i>Город: </i>{data[5] or "Не указан"}\n'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_name_button = types.InlineKeyboardButton('Поменять имя')
    change_city_button = types.InlineKeyboardButton('Указать или изменить город')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(change_name_button)
    markup.row(change_city_button)
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, profile_text, parse_mode='html', reply_markup=markup)
