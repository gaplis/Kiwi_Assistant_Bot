from telebot.asyncio_filters import SimpleCustomFilter
from datetime import datetime


class DateOrNoneFilter(SimpleCustomFilter):
    key = 'is_date_or_none'

    async def check(self, message):
        if message.text == 'Нет':
            return True
        else:
            try:
                datetime.strptime(message.text, '%d-%m-%Y')
                return True
            except ValueError:
                return False
