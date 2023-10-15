import json

from telebot.asyncio_filters import SimpleCustomFilter
from datetime import datetime


class DateOrNoneFilter(SimpleCustomFilter):
    key = 'is_date_or_none'

    async def check(self, message):
        if message.text.lower() == 'нет' or message.text.lower() == 'отмена':
            return True
        else:
            try:
                datetime.strptime(message.text, '%d-%m-%Y')
                return True
            except ValueError:
                return False


class IsValidIDFilter(SimpleCustomFilter):
    key = 'is_valid_id'

    async def check(self, message):
        if message.text.lower() == 'отмена':
            return True
        elif message.text.isdigit():
            with open('tasks.json', 'r', encoding='utf-8') as rf:
                json_file = json.load(rf)
            for json_dict in json_file:
                if json_dict['tg_id'] == message.from_user.id:
                    for i, item in enumerate(json_dict['tasks'], start=1):
                        if i == int(message.text):
                            return True
            else:
                return False
        else:
            return False


class IsCorrectLengthWord(SimpleCustomFilter):
    key = 'is_correct_length_word'

    async def check(self, message):
        return len(message.text) == 6
