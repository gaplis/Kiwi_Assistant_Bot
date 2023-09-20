from telebot.async_telebot import types
from datetime import datetime, timezone, timedelta

from config import OPEN_WEATHER_TOKEN

from utils.db import DataBase
from utils.weather import get_weather


async def weather_now(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        city = cursor.fetchone()[5]
    if city is None:
        weather_now_text = 'У тебя не указан город.\n' \
                           'Хочешь его указать?'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        change_city_button = types.InlineKeyboardButton('Указать город')
        main_menu_button = types.InlineKeyboardButton('Главное меню')
        markup.row(change_city_button)
        markup.row(main_menu_button)

        await bot.send_message(message.chat.id, weather_now_text, parse_mode='html', reply_markup=markup)
    else:
        weather = get_weather(f'{city}', OPEN_WEATHER_TOKEN)
        if 'message' in weather:
            weather_now_text = 'Похоже, ты указал несуществующий город или допустил опечатку.\n' \
                               'Попробуй указать правильный город.'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            change_city_button = types.InlineKeyboardButton('Изменить город')
            main_menu_button = types.InlineKeyboardButton('Главное меню')
            markup.row(change_city_button)
            markup.row(main_menu_button)

            await bot.send_message(message.chat.id, weather_now_text, parse_mode='html', reply_markup=markup)
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
            whats_now = weather["weather"][0]["main"]
            if whats_now in weather_descriptions:
                now = weather_descriptions[whats_now]
            else:
                now = 'Посмотри в окно, не пойму что там'
            tz = timezone(timedelta(seconds=weather['timezone']))
            weather_now_text = f'Погода в городе: {city}\n' \
                               f'Сейчас: {datetime.now(tz).strftime("%Y-%m-%d %H:%M")}\n' \
                               f'Температура: {weather["main"]["temp"]}°C, {now}\n' \
                               f'Ощущается как: {weather["main"]["feels_like"]}°C\n' \
                               f'Давление: {weather["main"]["pressure"]} мм.рт.ст.\n' \
                               f'Влажность: {weather["main"]["humidity"]}%\n' \
                               f'Скорость ветра: {weather["wind"]["speed"]} м/с\n' \
                               f'Облачность: {weather["clouds"]["all"]}%\n'
            if 'rain' in weather:
                weather_now_text += f'Осадков за последний час: {weather["rain"]["1h"]} мм.\n'
            if 'snow' in weather:
                weather_now_text += f'Снега за последний час: {weather["snow"]["1h"]} мм.\n'
            sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"], tz)
            sunset = datetime.fromtimestamp(weather["sys"]["sunset"], tz)
            weather_now_text += f'Восход солнца: {sunrise.strftime("%H:%M:%S")}\n' \
                                f'Заход солнца: {sunset.strftime("%H:%M:%S")}\n' \
                                f'Продолжительность дня: {sunset - sunrise}'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            change_city_button = types.InlineKeyboardButton('Погода на 5 дней')
            main_menu_button = types.InlineKeyboardButton('Главное меню')
            markup.row(change_city_button)
            markup.row(main_menu_button)

            await bot.send_message(message.chat.id, weather_now_text, parse_mode='html', reply_markup=markup)
