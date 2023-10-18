from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import TOKEN

from commands.start import start
from commands.profile import profile
from commands.not_found import not_found
from commands.change_city import change_city, cancel_change_city, ready_change_city
from commands.change_name import change_name, cancel_change_name, ready_change_name
from commands.diary import diary
from commands.add_task import add_task, cancel_add_task, get_task, get_deadline, incorrect_deadline
from commands.change_task import change_task, cancel_change_task, get_task_id, incorrect_task_id, get_new_data
from commands.delete_task import delete_task, cancel_delete_task, ready_delete_task, incorrect_del_task_id
from commands.weather_now import weather_now
from commands.weather_5_days import weather_5_days
from commands.search_in_google import search_in_google, cancel_search_in_google, ready_search_in_google
from commands.games import games
from commands.wordle_play import wordle_game, cancel_wordle_game, play_wordle_game, incorrect_length_word
from commands.statistics import statistics
from commands.ttt_play import ttt_game, cancel_ttt_game, play_ttt_game
from commands.tasks_notifications import on_tasks_notifications, off_tasks_notifications
from commands.morning_notifications import on_morning_notifications, off_morning_notifications

from utils.states import ChangeNameStates, ChangeCityStates, AddTaskStates, ChangeTaskStates, DeleteTaskStates, \
    SearchState, WordleGameState, TTTGameState
from utils.filters import DateOrNoneFilter, IsValidIDFilter, IsCorrectLengthWord
from utils.commands_lists import PROFILE, CHANGE_NAME, CHANGE_CITY, DIARY, ADD_TASK, CHANGE_TASK, DELETE_TASK, \
    MAIN_MENU, WEATHER_NOW, WEATHER_5_DAYS, SEARCH, GAMES, WORDLE_GAME, STATISTICS, TTT_GAME, ON_TASKS_NOTIFICATIONS, \
    OFF_TASKS_NOTIFICATIONS, ON_MORNING_NOTIFICATIONS, OFF_MORNING_NOTIFICATIONS

# ToDo: Разобраться с распределением комманд по файлам

# ToDo: проверить parse mode
bot = AsyncTeleBot(TOKEN, state_storage=StateMemoryStorage(), parse_mode='html')


# ToDo: проверить regexp, НЕТ - хорошо работает с кастомными фильтрами
@bot.message_handler(commands=['start'])
async def start_command(message):
    await start(message, bot)


@bot.message_handler(commands=['profile'])
async def profile_command(message):
    await profile(message, bot)


@bot.message_handler(commands=['change_name'])
async def change_name_command(message):
    await change_name(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_name_command(message):
    await cancel_change_name(message, bot)


@bot.message_handler(state=ChangeNameStates.new_name)
async def ready_for_change_name(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_name_command(message)

    await ready_change_name(message, bot)


@bot.message_handler(commands=['change_city'])
async def change_city_command(message):
    await change_city(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_city_command(message):
    await cancel_change_city(message, bot)


@bot.message_handler(state=ChangeCityStates.new_city)
async def ready_for_change_city(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_city_command(message)

    await ready_change_city(message, bot)


@bot.message_handler(commands=['diary'])
async def diary_command(message):
    await diary(message, bot)


@bot.message_handler(commands=['add_task'])
async def add_task_command(message):
    await add_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_add_task_command(message):
    await cancel_add_task(message, bot)


@bot.message_handler(state=AddTaskStates.task)
async def ready_for_get_task(message):
    if message.text.lower() == 'отмена':
        return await cancel_add_task_command(message)

    await get_task(message, bot)


@bot.message_handler(state=AddTaskStates.deadline, is_date_or_none=True)
async def ready_for_get_deadline(message):
    if message.text.lower() == 'отмена':
        return await cancel_add_task_command(message)

    await get_deadline(message, bot)


@bot.message_handler(state=AddTaskStates.deadline, is_date_or_none=False)
async def not_valid_deadline(message):
    await incorrect_deadline(message, bot)


@bot.message_handler(commands=['change_task'])
async def change_task_command(message):
    await change_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_change_task_command(message):
    await cancel_change_task(message, bot)


@bot.message_handler(state=ChangeTaskStates.id_task, is_valid_id=True)
async def ready_for_get_task_id(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_task_command(message)

    await get_task_id(message, bot)


@bot.message_handler(state=ChangeTaskStates.id_task, is_valid_id=False)
async def not_valid_task_id(message):
    await incorrect_task_id(message, bot)


@bot.message_handler(state=ChangeTaskStates.new_data)
async def ready_for_get_new_data(message):
    if message.text.lower() == 'отмена':
        return await cancel_change_task_command(message)

    await get_new_data(message, bot)


@bot.message_handler(commands=['delete_task'])
async def delete_task_command(message):
    await delete_task(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_delete_task_command(message):
    await cancel_delete_task(message, bot)


@bot.message_handler(state=DeleteTaskStates.id_task, is_valid_id=True)
async def ready_for_delete_task(message):
    if message.text.lower() == 'отмена':
        return await cancel_delete_task_command(message)

    await ready_delete_task(message, bot)


@bot.message_handler(state=DeleteTaskStates.id_task, is_valid_id=False)
async def not_valid_del_task_id(message):
    await incorrect_del_task_id(message, bot)


@bot.message_handler(commands=['weather_now'])
async def weather_now_command(message):
    await weather_now(message, bot)


@bot.message_handler(commands=['weather_5_days'])
async def weather_5_days_command(message):
    await weather_5_days(message, bot)


@bot.message_handler(commands=['search'])
async def search_in_google_command(message):
    await search_in_google(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_search_in_google_command(message):
    await cancel_search_in_google(message, bot)


@bot.message_handler(state=SearchState.search_data)
async def ready_search_in_google_command(message):
    if message.text.lower() == 'отмена':
        return await cancel_search_in_google_command(message)

    await ready_search_in_google(message, bot)


@bot.message_handler(commands=['games'])
async def games_command(message):
    await games(message, bot)


@bot.message_handler(commands=['wordle_game'])
async def wordle_game_command(message):
    await wordle_game(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_wordle_game_command(message):
    await cancel_wordle_game(message, bot)


@bot.message_handler(state=WordleGameState.game, is_correct_length_word=True)
async def play_wordle_game_command(message):
    if message.text.lower() == 'отмена':
        return await cancel_wordle_game_command(message)

    await play_wordle_game(message, bot)


@bot.message_handler(state=WordleGameState.game, is_correct_length_word=False)
async def incorrect_length_word_wordle_game(message):
    await incorrect_length_word(message, bot)


@bot.message_handler(commands=['statistics'])
async def statistics_command(message):
    await statistics(message, bot)


@bot.message_handler(commands=['tic_tac_toe_game'])
async def ttt_game_command(message):
    await ttt_game(message, bot)


@bot.message_handler(state="*", commands='cancel')
async def cancel_ttt_game_command(message):
    await cancel_ttt_game(message, bot)


@bot.message_handler(state=TTTGameState.game)
async def play_ttt_game_command(message):
    if message.text.lower() == 'отмена':
        return await cancel_ttt_game_command(message)

    await play_ttt_game(message, bot)


@bot.message_handler(commands=['on_tasks_notifications'])
async def on_tasks_notifications_command(message):
    await on_tasks_notifications(message, bot)


@bot.message_handler(commands=['off_tasks_notifications'])
async def off_tasks_notifications_command(message):
    await off_tasks_notifications(message, bot)


@bot.message_handler(commands=['on_morning_notifications'])
async def on_morning_notifications_command(message):
    await on_morning_notifications(message, bot)


@bot.message_handler(commands=['off_morning_notifications'])
async def off_morning_notifications_command(message):
    await off_morning_notifications(message, bot)


# ToDo: Посмотреть, как можно сделать иначе настройку сообщений
@bot.message_handler(content_types=['text'])
async def insert_text(message):
    command = message.text.lower()
    if command in PROFILE:
        await profile_command(message)
    elif command in CHANGE_NAME:
        await change_name_command(message)
    elif command in CHANGE_CITY:
        await change_city_command(message)
    elif command in DIARY:
        await diary_command(message)
    elif command in ADD_TASK:
        await add_task_command(message)
    elif command in CHANGE_TASK:
        await change_task_command(message)
    elif command in DELETE_TASK:
        await delete_task_command(message)
    elif command in MAIN_MENU:
        await start_command(message)
    elif command in WEATHER_5_DAYS:
        await weather_5_days_command(message)
    elif command in WEATHER_NOW or ('погода' in command and len(command.split()) > 1 and command not in WEATHER_5_DAYS):
        await weather_now_command(message)
    elif command in SEARCH:
        await search_in_google_command(message)
    elif command in GAMES:
        await games_command(message)
    elif command in WORDLE_GAME:
        await wordle_game_command(message)
    elif command in TTT_GAME:
        await ttt_game_command(message)
    elif command in STATISTICS:
        await statistics_command(message)
    elif command in ON_TASKS_NOTIFICATIONS:
        await on_tasks_notifications_command(message)
    elif command in OFF_TASKS_NOTIFICATIONS:
        await off_tasks_notifications_command(message)
    elif command in ON_MORNING_NOTIFICATIONS:
        await on_morning_notifications_command(message)
    elif command in OFF_MORNING_NOTIFICATIONS:
        await off_morning_notifications_command(message)
    else:
        await not_found_command(message)


@bot.message_handler()
async def not_found_command(message):
    await not_found(message, bot)
    await start_command(message)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(DateOrNoneFilter())
bot.add_custom_filter(IsValidIDFilter())
bot.add_custom_filter(IsCorrectLengthWord())
