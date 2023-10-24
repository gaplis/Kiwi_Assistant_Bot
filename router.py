from telebot.async_telebot import AsyncTeleBot

from commands import *


def router(bot: AsyncTeleBot):
    wordle_play.route(bot)
    ttt_play.route(bot)
    search_in_google.route(bot)
    add_task.route(bot)
    change_task.route(bot)
    delete_task.route(bot)
    change_name.route(bot)
    change_city.route(bot)
    main_menu.route(bot)
    user_profile.route(bot)
    diary.route(bot)
    weather_now.route(bot)
    weather_5_days.route(bot)
    games.route(bot)
    games_statistics.route(bot)
    tasks_notifications.route(bot)
    morning_notifications.route(bot)
    helps.route(bot)
    not_found.route(bot)
