import json

from telebot.async_telebot import AsyncTeleBot

from utils.markups import diary_markup


async def diary(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    for json_dict in json_file:
        if json_dict['tg_id'] == message.from_user.id:
            tasks_list = json_dict['tasks']
            if tasks_list:
                diary_text = f'<b>Ваши активные задачи:</b>\n'
                for i, item in enumerate(tasks_list, start=1):
                    diary_text += f'{i}: {item["task"]}\n' \
                                  f'Дата дедлайна: {"Не указано" if item["deadline"] is None else item["deadline"]}\n'
            else:
                diary_text = f'У вас нет активных задач.\n' \
                             f'Добавить?'
            break
    else:
        add_user = {
            "tg_id": message.from_user.id,
            "tasks": [],
            "notifications": False,
        }
        json_file.append(add_user)
        with open('tasks.json', 'w', encoding='utf-8') as wf:
            json.dump(json_file, wf, ensure_ascii=False, indent=2)
        diary_text = f'У вас нет активных задач.\n' \
                     f'Добавить?'

    await bot.send_message(message.chat.id, diary_text, reply_markup=diary_markup(message.from_user.id))


def route(bot: AsyncTeleBot):
    bot.register_message_handler(diary, diary_commands=True, pass_bot=True)
