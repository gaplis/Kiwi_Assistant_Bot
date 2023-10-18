from utils.db import DataBase
from utils.markups import profile_markup


async def profile(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.ALL)
        data = cursor.fetchone()
    profile_text = f'<b>Твой профиль</b>\n' \
                   f'<i>Имя: </i>{data[2]}\n' \
                   f'<i>Никнейм: </i>@{data[3]}\n' \
                   f'<i>id: </i>{data[0]}\n' \
                   f'<i>TGid: </i>{data[1]}\n' \
                   f'<i>Город: </i>{data[5] or "Не указан"}\n'

    await bot.send_message(message.chat.id, profile_text, reply_markup=profile_markup(data[1]))
