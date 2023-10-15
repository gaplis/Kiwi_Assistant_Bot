import json

from utils.states import DeleteTaskStates
from utils.markups import cancel_markup, main_menu_markup


async def delete_task(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    for json_dict in json_file:
        if json_dict['tg_id'] == message.from_user.id:
            tasks_list = json_dict['tasks']
            if tasks_list:
                choice_task_text = 'Напиши номер задачи, которую хочешь удалить:\n'
                for i, item in enumerate(tasks_list, start=1):
                    choice_task_text += f'{i}: {item["task"]}\n'

                await bot.set_state(message.from_user.id, DeleteTaskStates.id_task, message.chat.id)
                return await bot.send_message(message.chat.id, choice_task_text, reply_markup=cancel_markup())
    else:
        tasks_not_found_text = 'У тебя нет активных задач, удалять нечего.'

        await bot.send_message(message.chat.id, tasks_not_found_text, reply_markup=main_menu_markup())


async def cancel_delete_task(message, bot):
    cancel_text = "Если нужно будет удалить задачу, то возвращайся 😇"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def ready_delete_task(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    with open('tasks.json', 'w', encoding='utf-8') as wf:
        for json_dict in json_file:
            if json_dict['tg_id'] == message.from_user.id:
                json_dict['tasks'].pop(int(message.text) - 1)
                json.dump(json_file, wf, ensure_ascii=False, indent=2)
                break

    delete_task_text = f'<b>Готово, удалена задача {message.text}:\n</b>'

    await bot.send_message(message.chat.id, delete_task_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def incorrect_del_task_id(message, bot):
    error_text = 'Похоже, ты указал задачу, которой нет, или написал не число.\n' \
                 'Попробуй снова, ты должен ввести номер задачи'

    await bot.send_message(message.chat.id, error_text, reply_markup=cancel_markup())
