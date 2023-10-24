import json

from telebot.async_telebot import AsyncTeleBot

from utils.markups import main_menu_markup


async def on_tasks_notifications(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    for json_dict in json_file:
        if json_dict['tg_id'] == message.from_user.id:
            json_dict['notifications'] = True

    with open('tasks.json', 'w', encoding='utf-8') as wf:
        json.dump(json_file, wf, ensure_ascii=False, indent=2)

    on_text = f'Уведомления о задачах включены!'

    await bot.send_message(message.chat.id, on_text, reply_markup=main_menu_markup())


async def off_tasks_notifications(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    for json_dict in json_file:
        if json_dict['tg_id'] == message.from_user.id:
            json_dict['notifications'] = False

    with open('tasks.json', 'w', encoding='utf-8') as wf:
        json.dump(json_file, wf, ensure_ascii=False, indent=2)

    off_text = f'Уведомления о задачах выключены!'

    await bot.send_message(message.chat.id, off_text, reply_markup=main_menu_markup())


def route(bot: AsyncTeleBot):
    bot.register_message_handler(on_tasks_notifications, on_task_notifications_commands=True, pass_bot=True)
    bot.register_message_handler(off_tasks_notifications, off_task_notifications_commands=True, pass_bot=True)
