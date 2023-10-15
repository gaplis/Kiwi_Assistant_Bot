from telebot.async_telebot import types
from telebot.util import quick_markup


def start_markup():
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

    return markup


def profile_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_name_button = types.InlineKeyboardButton('Поменять имя')
    change_city_button = types.InlineKeyboardButton('Указать или изменить город')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(change_name_button)
    markup.row(change_city_button)
    markup.row(main_menu_button)

    return markup


def cancel_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    return markup


def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    return markup


def diary_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_task_button = types.InlineKeyboardButton('Добавить задачу')
    change_task_button = types.InlineKeyboardButton('Изменить задачу')
    delete_task_button = types.InlineKeyboardButton('Удалить задачу')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(add_task_button)
    markup.row(change_task_button)
    markup.row(delete_task_button)
    markup.row(main_menu_button)

    return markup


def get_more_task_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    more_task_button = types.InlineKeyboardButton('Добавить ещё задачу')
    markup.row(main_menu_button)
    markup.row(more_task_button)

    return markup


def weather_city_is_none_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_city_button = types.InlineKeyboardButton('Указать город')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(change_city_button)
    markup.row(main_menu_button)

    return markup


def weather_incorrect_city_markup(is_db):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_city_button = types.InlineKeyboardButton('Изменить город')
    main_menu_button = types.InlineKeyboardButton('Главное меню')

    if is_db:
        markup.row(change_city_button)
        markup.row(main_menu_button)
    else:
        markup.row(main_menu_button)

    return markup


def weather_ready_markup(now):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_5_days_button = types.InlineKeyboardButton('Погода на 5 дней')
    main_menu_button = types.InlineKeyboardButton('Главное меню')

    if now:
        markup.row(weather_5_days_button)
        markup.row(main_menu_button)
    else:
        markup.row(main_menu_button)

    return markup


def more_search_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    more_search_button = types.InlineKeyboardButton('Найти ещё')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(more_search_button)
    markup.row(main_menu_button)

    return markup


def data_search_inline_markup(urls):
    markup = quick_markup({
        '1': {'url': f'{urls[0]["url"]}'},
        '2': {'url': f'{urls[1]["url"]}'},
        '3': {'url': f'{urls[2]["url"]}'},
        'Поиск в Google': {'url': f'{urls[3]["url"]}'},
    }, row_width=3)

    return markup


def games_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tic_tac_toe_button = types.InlineKeyboardButton('Крестики-нолики')
    wordle_button = types.InlineKeyboardButton('Вордли')
    statistics_button = types.InlineKeyboardButton('Моя статистика')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(tic_tac_toe_button)
    markup.row(wordle_button)
    markup.row(statistics_button)
    markup.row(main_menu_button)

    return markup
