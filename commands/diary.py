from telebot.async_telebot import types
import json


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
        }
        json_file.append(add_user)
        with open('tasks.json', 'w', encoding='utf-8') as wf:
            json.dump(json_file, wf, ensure_ascii=False, indent=2)
        diary_text = f'У вас нет активных задач.\n' \
                     f'Добавить?'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_task_button = types.InlineKeyboardButton('Добавить задачу')
    change_task_button = types.InlineKeyboardButton('Изменить задачу')
    delete_task_button = types.InlineKeyboardButton('Удалить задачу')
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(add_task_button)
    markup.row(change_task_button)
    markup.row(delete_task_button)
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, diary_text, parse_mode='html', reply_markup=markup)
