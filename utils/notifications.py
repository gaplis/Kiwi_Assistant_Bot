from telebot.async_telebot import AsyncTeleBot


async def tasks_notifications(bot: AsyncTeleBot):
    while True:
        pass


async def good_morning_notifications(bot: AsyncTeleBot):
    while True:
        pass


async def running(bot):
    await tasks_notifications(bot)
    await good_morning_notifications(bot)
