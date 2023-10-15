from datetime import datetime, timezone, timedelta

from config import OPEN_WEATHER_TOKEN

from utils.db import DataBase
from utils.weather import get_weather_5_days, WEATHER_DESCRIPTIONS
from utils.markups import weather_city_is_none_markup, weather_incorrect_city_markup, weather_ready_markup


async def weather_5_days(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        city = cursor.fetchone()[5]
    if city is not None:
        weather = get_weather_5_days(f'{city}', OPEN_WEATHER_TOKEN)
        if weather['message'] != 0:
            weather_5_days_text = 'Похоже, ты указал несуществующий город или допустил опечатку.\n' \
                                  'Попробуй указать правильный город.'

            await bot.send_message(message.chat.id, weather_5_days_text,
                                   reply_markup=weather_incorrect_city_markup(True))
        else:
            weather_5_days_text = f'Погода на 5 дней в городе: {city}\n'
            for i in range(0, len(weather["list"]), 2):
                tz = timezone(timedelta(seconds=weather['city']['timezone']))
                dt = str(datetime.fromtimestamp(weather["list"][i]["dt"], tz).strftime("%Y-%m-%d %H:%M"))
                if dt.split()[0] not in weather_5_days_text:
                    weather_5_days_text += f'\nДата: {dt.split()[0]}\n'
                weather_5_days_text += f'🕓Время: {dt.split()[1]}\n'
                whats_now = weather["list"][i]["weather"][0]["main"]
                if whats_now in WEATHER_DESCRIPTIONS:
                    now = WEATHER_DESCRIPTIONS[whats_now]
                else:
                    now = 'Посмотри в окно, не пойму что там'
                weather_5_days_text += f'Температура: {weather["list"][i]["main"]["temp"]}°C, {now}\n'

            await bot.send_message(message.chat.id, weather_5_days_text, reply_markup=weather_ready_markup(False))
    else:
        weather_5_days_text = 'У тебя не указан город.\n' \
                              'Хочешь его указать?'

        await bot.send_message(message.chat.id, weather_5_days_text, reply_markup=weather_city_is_none_markup())

