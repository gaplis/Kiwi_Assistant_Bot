async def not_found(message, bot):
    not_found_text = f'<i>Пока что не знаю, что делать с этой информацией...\n</i>'
    await bot.send_message(message.chat.id, not_found_text, parse_mode='html')
