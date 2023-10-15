import json

from utils.states import AddTaskStates
from utils.markups import get_more_task_markup, cancel_markup, main_menu_markup


async def add_task(message, bot):
    task_text = 'Напиши свою задачу'

    await bot.set_state(message.from_user.id, AddTaskStates.task, message.chat.id)
    await bot.send_message(message.chat.id, task_text, reply_markup=cancel_markup())


async def cancel_add_task(message, bot):
    cancel_text = "Если что, то ты всегда можешь вернуться и добавить задачу"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def get_task(message, bot):
    deadline_text = 'А теперь укажи дату в формате "DD-MM-YYYY", до которой задачу необходимо выполнить ' \
                    'или напиши "Нет", если дата не нужна'

    await bot.send_message(message.chat.id, deadline_text, reply_markup=cancel_markup())
    await bot.set_state(message.from_user.id, AddTaskStates.deadline, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task'] = message.text


async def get_deadline(message, bot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        task = data["task"]
        deadline = None if message.text.lower() == "нет" else message.text
        task_dict = {'task': task, 'deadline': deadline}
        with open('tasks.json', 'r', encoding='utf-8') as rf:
            json_file = json.load(rf)
        with open('tasks.json', 'w', encoding='utf-8') as wf:
            for json_dict in json_file:
                if json_dict['tg_id'] == message.from_user.id:
                    json_dict['tasks'].append(task_dict)
                    json.dump(json_file, wf, ensure_ascii=False, indent=2)
                    break

    add_task_text = f'<b>Готово, добавлена задача:\n</b>' \
                    f'{task}\n' \
                    f'Срок до: {"Не указано" if deadline is None else deadline}'

    await bot.send_message(message.chat.id, add_task_text, reply_markup=get_more_task_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def incorrect_deadline(message, bot):
    error_text = 'Нужно указывать дату в формате "DD-MM-YYYY", ' \
                 'либо ты указал неверную дату, попробуй ещё раз или напиши "Нет"'
    await bot.send_message(message.chat.id, error_text, reply_markup=cancel_markup())
