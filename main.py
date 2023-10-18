import asyncio

from bot import bot
from utils.notifications import running_notifications


async def main():
    start_bot = asyncio.create_task(bot.polling(none_stop=True))
    start_notifications = asyncio.create_task(running_notifications(bot))
    await start_bot
    await start_notifications


if __name__ == '__main__':
    asyncio.run(main())
