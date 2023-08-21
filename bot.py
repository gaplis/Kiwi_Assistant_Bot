from telebot.async_telebot import AsyncTeleBot, types
from config import TOKEN, host, port, user_bd, password_bd, name_bd
import pymysql

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def start_command(message):
    try:
        connection_bd = pymysql.connect(
            host=host,
            port=port,
            user=user_bd,
            password=password_bd,
            database=name_bd,
        )
        print('Успешно подключились к БД')
        try:
            with connection_bd.cursor() as cursor:
                find_user = f"SELECT tg_id FROM {name_bd}.users WHERE tg_id = {message.from_user.id}"
                cursor.execute(find_user)
                if cursor.fetchone() is None:
                    insert_data = f"INSERT INTO {name_bd}.users " \
                                  f"(tg_id, first_name, username, language_code, chat_id) " \
                                  f"VALUES ({message.from_user.id}, '{message.from_user.first_name}', " \
                                  f"'{message.from_user.username}', '{message.from_user.language_code}', " \
                                  f"{message.chat.id});"
                    cursor.execute(insert_data)
                    connection_bd.commit()
                    print('Успешно добавили данные в БД')
                else:
                    print('Данный пользователь уже есть в БД')
        except Exception as ex:
            print(ex)
            print('Неуспешно добавили данные в БД')
        finally:
            connection_bd.close()
            print('Отключились от БД')
    except Exception as ex:
        print(ex)
        print('Неуспешно подключились к БД')

    start_text = f'<b>Привет, {message.from_user.first_name}! Это Киви, я бот-ассистент. 😊</b>\n' \
                 f'<i>Посмотри меню или попробуй что-нибудь написать мне. 😉</i> '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton('Профиль')
    markup.row(profile_button)

    await bot.send_message(message.chat.id, start_text, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['profile'])
async def profile_command(message):
    try:
        connection_bd = pymysql.connect(
            host=host,
            port=port,
            user=user_bd,
            password=password_bd,
            database=name_bd,
        )
        print('Успешно подключились к БД')
        with connection_bd.cursor() as cursor:
            find_user = f"SELECT id FROM {name_bd}.users WHERE tg_id = {message.from_user.id}"
            cursor.execute(find_user)
            u_id = cursor.fetchone()[0]
            print(f'Получили id {u_id} у пользователя @{message.from_user.username}')
        connection_bd.close()
        print('Отключились от БД')
    except Exception as ex:
        print(ex)
        print('Неуспешно подключились к БД')

    profile_text = f'<b>Ваш профиль</b>\n' \
                   f'<i>Имя: </i>{message.from_user.first_name}\n' \
                   f'<i>Никнейм: </i>@{message.from_user.username}\n' \
                   f'<i>id: </i>{u_id}\n' \
                   f'<i>TGid: </i>{message.from_user.id}\n'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_name_button = types.InlineKeyboardButton('Поменять имя')
    markup.row(change_name_button)
    await bot.send_message(message.chat.id, profile_text, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['change'])
async def change_name_command(message):
    pass


@bot.message_handler(content_types=['text'])
async def insert_text(message):
    match message.text.lower():
        case 'профиль':
            await profile_command(message)
        case 'поменять имя':
            await change_name_command(message)
        case _:
            await start_command(message)
