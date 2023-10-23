from telebot.asyncio_filters import SimpleCustomFilter
from telebot.async_telebot import types, AsyncTeleBot
from utils.commands_lists import PROFILE, CHANGE_NAME, CHANGE_CITY, DIARY, ADD_TASK, CHANGE_TASK, DELETE_TASK, \
    MAIN_MENU, WEATHER_NOW, WEATHER_5_DAYS, SEARCH, GAMES, WORDLE_GAME, STATISTICS, TTT_GAME, ON_TASKS_NOTIFICATIONS, \
    OFF_TASKS_NOTIFICATIONS, ON_MORNING_NOTIFICATIONS, OFF_MORNING_NOTIFICATIONS, HELP, CANCEL, GIVE_UP


class MainMenuCommandsFilter(SimpleCustomFilter):
    key = 'main_menu_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in MAIN_MENU


class ProfileCommandsFilter(SimpleCustomFilter):
    key = 'profile_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in PROFILE


class ChangeNameCommandsFilter(SimpleCustomFilter):
    key = 'change_name_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in CHANGE_NAME


class ChangeCityCommandsFilter(SimpleCustomFilter):
    key = 'change_city_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in CHANGE_CITY


class DiaryCommandsFilter(SimpleCustomFilter):
    key = 'diary_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in DIARY


class AddTaskCommandsFilter(SimpleCustomFilter):
    key = 'add_task_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in ADD_TASK


class ChangeTaskCommandsFilter(SimpleCustomFilter):
    key = 'change_task_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in CHANGE_TASK


class DeleteTaskCommandsFilter(SimpleCustomFilter):
    key = 'delete_task_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in DELETE_TASK


class WeatherNowCommandsFilter(SimpleCustomFilter):
    key = 'weather_now_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in WEATHER_NOW \
            or ('погода' in command and len(command.split()) > 1 and command not in WEATHER_5_DAYS)


class Weather5DaysCommandsFilter(SimpleCustomFilter):
    key = 'weather_5_days_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in WEATHER_5_DAYS


class SearchCommandsFilter(SimpleCustomFilter):
    key = 'search_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in SEARCH


class GamesCommandsFilter(SimpleCustomFilter):
    key = 'games_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in GAMES


class WordleGameCommandsFilter(SimpleCustomFilter):
    key = 'wordle_game_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in WORDLE_GAME


class TTTGameCommandsFilter(SimpleCustomFilter):
    key = 'ttt_game_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in TTT_GAME


class StatisticsCommandsFilter(SimpleCustomFilter):
    key = 'statistics_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in STATISTICS


class OnTaskNotificationsCommandsFilter(SimpleCustomFilter):
    key = 'on_task_notifications_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in ON_TASKS_NOTIFICATIONS


class OffTaskNotificationsCommandsFilter(SimpleCustomFilter):
    key = 'off_task_notifications_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in OFF_TASKS_NOTIFICATIONS


class OnMorningNotificationsCommandsFilter(SimpleCustomFilter):
    key = 'on_morning_notifications_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in ON_MORNING_NOTIFICATIONS


class OffMorningNotificationsCommandsFilter(SimpleCustomFilter):
    key = 'off_morning_notifications_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in OFF_MORNING_NOTIFICATIONS


class HelpCommandsFilter(SimpleCustomFilter):
    key = 'help_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in HELP


class CancelCommandsFilter(SimpleCustomFilter):
    key = 'cancel_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in CANCEL


class GiveUpCommandsFilter(SimpleCustomFilter):
    key = 'give_up_commands'

    async def check(self, message: types.Message):
        command = message.text.lower()
        return command in GIVE_UP


def register_commands_filters(bot: AsyncTeleBot):
    bot.add_custom_filter(MainMenuCommandsFilter())
    bot.add_custom_filter(ProfileCommandsFilter())
    bot.add_custom_filter(ChangeNameCommandsFilter())
    bot.add_custom_filter(ChangeCityCommandsFilter())
    bot.add_custom_filter(DiaryCommandsFilter())
    bot.add_custom_filter(AddTaskCommandsFilter())
    bot.add_custom_filter(ChangeTaskCommandsFilter())
    bot.add_custom_filter(DeleteTaskCommandsFilter())
    bot.add_custom_filter(WeatherNowCommandsFilter())
    bot.add_custom_filter(Weather5DaysCommandsFilter())
    bot.add_custom_filter(SearchCommandsFilter())
    bot.add_custom_filter(GamesCommandsFilter())
    bot.add_custom_filter(WordleGameCommandsFilter())
    bot.add_custom_filter(TTTGameCommandsFilter())
    bot.add_custom_filter(StatisticsCommandsFilter())
    bot.add_custom_filter(OnTaskNotificationsCommandsFilter())
    bot.add_custom_filter(OffTaskNotificationsCommandsFilter())
    bot.add_custom_filter(OnMorningNotificationsCommandsFilter())
    bot.add_custom_filter(OffMorningNotificationsCommandsFilter())
    bot.add_custom_filter(HelpCommandsFilter())
    bot.add_custom_filter(CancelCommandsFilter())
    bot.add_custom_filter(GiveUpCommandsFilter())
