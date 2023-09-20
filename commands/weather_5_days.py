from telebot.async_telebot import types
from datetime import datetime, timezone, timedelta

from config import OPEN_WEATHER_TOKEN

from utils.db import DataBase
from utils.weather import get_weather_5_days


async def weather_5_days(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        city = cursor.fetchone()[5]
    if city is None:
        weather_5_days_text = 'У тебя не указан город.\n' \
                              'Хочешь его указать?'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        change_city_button = types.InlineKeyboardButton('Указать город')
        main_menu_button = types.InlineKeyboardButton('Главное меню')
        markup.row(change_city_button)
        markup.row(main_menu_button)

        await bot.send_message(message.chat.id, weather_5_days_text, parse_mode='html', reply_markup=markup)
    else:
        weather = get_weather_5_days(f'{city}', OPEN_WEATHER_TOKEN)
        if weather['message'] != 0:
            print(weather)
            weather_5_days_text = 'Похоже, ты указал несуществующий город или допустил опечатку.\n' \
                                  'Попробуй указать правильный город.'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            change_city_button = types.InlineKeyboardButton('Изменить город')
            main_menu_button = types.InlineKeyboardButton('Главное меню')
            markup.row(change_city_button)
            markup.row(main_menu_button)

            await bot.send_message(message.chat.id, weather_5_days_text, parse_mode='html', reply_markup=markup)
        else:
            weather_descriptions = {
                "Clear": "Ясно☀️",
                "Clouds": "Облачно☁️",
                "Rain": "Дождь🌧️",
                "Drizzle": "Мелкий дождь🌧️",
                "Thunderstorm": "Гроза⛈️",
                "Snow": "Снег🌨️",
                "Mist": "Туман🌫️",
            }
            weather_5_days_text = f'Погода на 5 дней в городе: {city}\n'
            for i in range(0, len(weather["list"]), 2):
                tz = timezone(timedelta(seconds=weather['city']['timezone']))
                dt = str(datetime.fromtimestamp(weather["list"][i]["dt"], tz).strftime("%Y-%m-%d %H:%M"))
                if dt.split()[0] not in weather_5_days_text:
                    weather_5_days_text += f'\nДата: {dt.split()[0]}\n'
                weather_5_days_text += f'🕓Время: {dt.split()[1]}\n'
                whats_now = weather["list"][i]["weather"][0]["main"]
                if whats_now in weather_descriptions:
                    now = weather_descriptions[whats_now]
                else:
                    now = 'Посмотри в окно, не пойму что там'
                weather_5_days_text += f'Температура: {weather["list"][i]["main"]["temp"]}°C, {now}\n'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            main_menu_button = types.InlineKeyboardButton('Главное меню')
            markup.row(main_menu_button)

            await bot.send_message(message.chat.id, weather_5_days_text, parse_mode='html', reply_markup=markup)
