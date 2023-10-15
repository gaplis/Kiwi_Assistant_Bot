from utils.markups import games_markup


async def games(message, bot):
    games_text = f'Во что хочешь поиграть?'

    await bot.send_message(message.chat.id, games_text, reply_markup=games_markup())
