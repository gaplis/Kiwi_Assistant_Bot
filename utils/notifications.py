import asyncio
import json
from datetime import datetime, timedelta, timezone
from utils.db import DataBase
from utils.weather import get_weather_5_days, WEATHER_DESCRIPTIONS
from config import OPEN_WEATHER_TOKEN

from telebot.async_telebot import AsyncTeleBot


async def tasks_notifications(bot: AsyncTeleBot):
    while True:
        with open('tasks.json', 'r', encoding='utf-8') as rf:
            json_file = json.load(rf)
        for json_dict in json_file:
            if json_dict['notifications']:
                tasks_list = json_dict['tasks']
                if tasks_list:
                    for item in tasks_list:
                        get_date = None if item['deadline'] is None else item['deadline'].split('-')
                        if get_date is not None:
                            deadline = datetime(day=int(get_date[0]), month=int(get_date[1]),
                                                year=int(get_date[2])).date()
                            today = datetime.today().date()
                            if deadline == today:
                                notification_text = f'<b>Сегодня дедлайн задачи:\n</b>' \
                                                    f'{item["task"]}'
                                await bot.send_message(json_dict['tg_id'], notification_text)
                            elif deadline == today + timedelta(days=1):
                                notification_text = f'<b>Завтра дедлайн задачи:\n</b>' \
                                                    f'{item["task"]}'
                                await bot.send_message(json_dict['tg_id'], notification_text)
                            elif deadline == today + timedelta(days=3):
                                notification_text = f'<b>Через 3 дня дедлайн задачи:\n</b>' \
                                                    f'{item["task"]}'
                                await bot.send_message(json_dict['tg_id'], notification_text)
                            elif deadline == today + timedelta(days=7):
                                notification_text = f'<b>Через 7 дней дедлайн задачи:\n</b>' \
                                                    f'{item["task"]}'
                                await bot.send_message(json_dict['tg_id'], notification_text)

        now = datetime.now()
        delta = now + timedelta(days=1)
        tomorrow = datetime(day=delta.day, month=delta.month, year=delta.year, hour=9, second=30)
        sleep_seconds = tomorrow - now
        await asyncio.sleep(sleep_seconds.total_seconds())


async def good_morning_notifications(bot: AsyncTeleBot):
    while True:
        db = DataBase()
        with db as cursor:
            db.find_user_for_notifications(db.TG_ID, db.F_NAME, db.U_CITY, db.NOTIFICATIONS, db.TIMEZONE)
            users = cursor.fetchall()
            for user in users:
                notifications = user[3]
                if notifications == 1:
                    tz = timezone(timedelta(seconds=user[4]))
                    now_hour = datetime.now(tz=tz).time().hour
                    if now_hour == 9:
                        tg_id = user[0]
                        name = user[1]
                        city = user[2]
                        date_now = datetime.today().date().strftime('%d-%m-%Y')

                        good_morning_text = f'<b>Доброе утро, {name}!</b>\n' \
                                            f'Сегодня {date_now}\n\n'
                        if city is not None:
                            weather = get_weather_5_days(f'{city}', OPEN_WEATHER_TOKEN)
                            if weather['message'] == 0:
                                good_morning_text += f'<b>Погода на сегодня:</b>\n'
                                for i in range(0, 8):
                                    time = str(datetime.fromtimestamp(weather["list"][i]["dt"], tz)
                                               .strftime("%H:%M"))
                                    good_morning_text += f'🕓Время: {time}\n'
                                    whats_now = weather["list"][i]["weather"][0]["main"]
                                    if whats_now in WEATHER_DESCRIPTIONS:
                                        now = WEATHER_DESCRIPTIONS[whats_now]
                                    else:
                                        now = 'Посмотри в окно, не пойму что там'
                                    good_morning_text += f'{now}, {weather["list"][i]["main"]["temp"]}°C\n'
                            else:
                                good_morning_text += 'Похоже, указанного тобой города не существует, ' \
                                                     'поэтому погоду не скажу 😒\n'
                        else:
                            good_morning_text += 'У тебя не указан город, поэтому погоду не скажу 😒\n'

                        with open('tasks.json', 'r', encoding='utf-8') as rf:
                            json_file = json.load(rf)
                        for json_dict in json_file:
                            if json_dict['tg_id'] == tg_id:
                                tasks_list = json_dict['tasks']
                                if tasks_list:
                                    good_morning_text += f'\n<b>Твои активные задачи:</b>\n'
                                    for i, item in enumerate(tasks_list, start=1):
                                        good_morning_text += f'{i}: {item["task"]}\n' \
                                                             f'Дата дедлайна: ' \
                                                             f'{"Не указано" if item["deadline"] is None else item["deadline"]}\n'
                                    break
                        else:
                            good_morning_text += f'\nАктивных задач у тебя нет'

                        await bot.send_message(tg_id, good_morning_text)

        now = datetime.now()
        delta = now + timedelta(hours=1)
        next_hour = datetime(day=delta.day, month=delta.month, year=delta.year, hour=delta.hour, second=30)
        sleep_seconds = next_hour - now
        await asyncio.sleep(sleep_seconds.total_seconds())


async def running_notifications(bot):
    tasks = asyncio.create_task(tasks_notifications(bot))
    good_morning = asyncio.create_task(good_morning_notifications(bot))
    await tasks
    await good_morning
