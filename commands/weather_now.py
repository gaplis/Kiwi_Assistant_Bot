from datetime import datetime, timezone, timedelta

from config import OPEN_WEATHER_TOKEN

from utils.db import DataBase
from utils.weather import get_weather, WEATHER_DESCRIPTIONS
from utils.markups import weather_city_is_none_markup, weather_incorrect_city_markup, weather_ready_markup


async def weather_now(message, bot):
    if len(message.text.split()) > 1:
        city = " ".join(message.text.split()[1::]).title()
        is_db = False
    else:
        db = DataBase()
        with db as cursor:
            db.find_user(message.from_user.id, db.ALL)
            city = cursor.fetchone()[5]
            is_db = True
    if city is not None:
        weather = get_weather(f'{city}', OPEN_WEATHER_TOKEN)
        if 'message' in weather:
            incorrect_city_text = 'Похоже, ты указал несуществующий город или допустил опечатку.\n' \
                                  'Попробуй указать правильный город.'

            await bot.send_message(message.chat.id, incorrect_city_text,
                                   parse_mode='html', reply_markup=weather_incorrect_city_markup(is_db))
        else:
            whats_now = weather["weather"][0]["main"]
            if whats_now in WEATHER_DESCRIPTIONS:
                now = WEATHER_DESCRIPTIONS[whats_now]
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

            await bot.send_message(message.chat.id, weather_now_text,
                                   parse_mode='html', reply_markup=weather_ready_markup(True))
    else:
        city_is_none_text = 'У тебя не указан город.\n' \
                            'Хочешь его указать?'

        await bot.send_message(message.chat.id, city_is_none_text,
                               parse_mode='html', reply_markup=weather_city_is_none_markup())
