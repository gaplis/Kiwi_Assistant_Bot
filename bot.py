from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import TOKEN

from commands.main_menu import main_menu
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
from commands.helps import helps

from utils.states import ChangeNameStates, ChangeCityStates, AddTaskStates, ChangeTaskStates, DeleteTaskStates, \
    SearchState, WordleGameState, TTTGameState
from utils.filters import register_filters
from utils.commands_filters import register_commands_filters

# ToDo: Разобраться с распределением комманд по файлам

bot = AsyncTeleBot(TOKEN, state_storage=StateMemoryStorage(), parse_mode='html')

bot.register_message_handler(wordle_game, wordle_game_commands=True, pass_bot=True)
bot.register_message_handler(cancel_wordle_game, state=WordleGameState.game, give_up_commands=True, pass_bot=True)
bot.register_message_handler(play_wordle_game, state=WordleGameState.game, is_correct_length_word=True, pass_bot=True)
bot.register_message_handler(incorrect_length_word, state=WordleGameState.game, is_correct_length_word=False,
                             pass_bot=True)

bot.register_message_handler(ttt_game, ttt_game_commands=True, pass_bot=True)
bot.register_message_handler(cancel_ttt_game, state=TTTGameState.game, give_up_commands=True, pass_bot=True)
bot.register_message_handler(play_ttt_game, state=TTTGameState.game, pass_bot=True)

bot.register_message_handler(search_in_google, search_commands=True, pass_bot=True)
bot.register_message_handler(cancel_search_in_google, state=SearchState.search_data, cancel_commands=True,
                             pass_bot=True)
bot.register_message_handler(ready_search_in_google, state=SearchState.search_data, pass_bot=True)

bot.register_message_handler(add_task, add_task_commands=True, pass_bot=True)
bot.register_message_handler(cancel_add_task, state=AddTaskStates.task, cancel_commands=True, pass_bot=True)
bot.register_message_handler(cancel_add_task, state=AddTaskStates.deadline, cancel_commands=True, pass_bot=True)
bot.register_message_handler(get_task, state=AddTaskStates.task, pass_bot=True)
bot.register_message_handler(get_deadline, state=AddTaskStates.deadline, is_date_or_none=True, pass_bot=True)
bot.register_message_handler(incorrect_deadline, state=AddTaskStates.deadline, is_date_or_none=False, pass_bot=True)

bot.register_message_handler(change_task, change_task_commands=True, pass_bot=True)
bot.register_message_handler(cancel_change_task, state=ChangeTaskStates.id_task, cancel_commands=True, pass_bot=True)
bot.register_message_handler(cancel_change_task, state=ChangeTaskStates.new_data, cancel_commands=True, pass_bot=True)
bot.register_message_handler(get_task_id, state=ChangeTaskStates.id_task, is_valid_id=True, pass_bot=True)
bot.register_message_handler(incorrect_task_id, state=ChangeTaskStates.id_task, is_valid_id=False, pass_bot=True)
bot.register_message_handler(get_new_data, state=ChangeTaskStates.new_data, pass_bot=True)

bot.register_message_handler(delete_task, delete_task_commands=True, pass_bot=True)
bot.register_message_handler(cancel_delete_task, state=DeleteTaskStates.id_task, cancel_commands=True, pass_bot=True)
bot.register_message_handler(ready_delete_task, state=DeleteTaskStates.id_task, is_valid_id=True, pass_bot=True)
bot.register_message_handler(incorrect_del_task_id, state=DeleteTaskStates.id_task, is_valid_id=False, pass_bot=True)

bot.register_message_handler(change_name, change_name_commands=True, pass_bot=True)
bot.register_message_handler(cancel_change_name, state=ChangeNameStates.new_name, cancel_commands=True, pass_bot=True)
bot.register_message_handler(ready_change_name, state=ChangeNameStates.new_name, pass_bot=True)

bot.register_message_handler(change_city, change_city_commands=True, pass_bot=True)
bot.register_message_handler(cancel_change_city, state=ChangeCityStates.new_city, cancel_commands=True, pass_bot=True)
bot.register_message_handler(ready_change_city, state=ChangeCityStates.new_city, pass_bot=True)

bot.register_message_handler(main_menu, main_menu_commands=True, pass_bot=True)
bot.register_message_handler(profile, profile_commands=True, pass_bot=True)
bot.register_message_handler(diary, diary_commands=True, pass_bot=True)
bot.register_message_handler(weather_now, weather_now_commands=True, pass_bot=True)
bot.register_message_handler(weather_5_days, weather_5_days_commands=True, pass_bot=True)
bot.register_message_handler(games, games_commands=True, pass_bot=True)
bot.register_message_handler(statistics, statistics_commands=True, pass_bot=True)
bot.register_message_handler(on_tasks_notifications, on_task_notifications_commands=True, pass_bot=True)
bot.register_message_handler(off_tasks_notifications, off_task_notifications_commands=True, pass_bot=True)
bot.register_message_handler(on_morning_notifications, on_morning_notifications_commands=True, pass_bot=True)
bot.register_message_handler(off_morning_notifications, off_morning_notifications_commands=True, pass_bot=True)
bot.register_message_handler(helps, help_commands=True, pass_bot=True)
bot.register_message_handler(not_found, pass_bot=True)

register_filters(bot)
register_commands_filters(bot)
