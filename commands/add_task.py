from telebot.async_telebot import types
from utils.states import AddTaskStates
import json


async def add_task(message, bot):
    task_text = 'Напиши свою задачу'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    await bot.set_state(message.from_user.id, AddTaskStates.task, message.chat.id)
    await bot.send_message(message.chat.id, task_text, parse_mode='html', reply_markup=markup)


async def cancel_add_task(message, bot):
    cancel_text = "Если что, то ты всегда можешь вернуться и добавить задачу"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, cancel_text, parse_mode='html', reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def get_task(message, bot):
    deadline_text = 'А теперь укажи дату в формате "DD-MM-YYYY", до которой задачу необходимо выполнить ' \
                    'или напиши "Нет", если дата не нужна'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    await bot.send_message(message.chat.id, deadline_text, parse_mode='html', reply_markup=markup)
    await bot.set_state(message.from_user.id, AddTaskStates.deadline, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task'] = message.text


async def get_deadline(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    more_task_button = types.InlineKeyboardButton('Добавить ещё задачу')
    markup.row(main_menu_button)
    markup.row(more_task_button)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        deadline = None if message.text.lower() == "нет" else message.text
        task_dict = {'task': data["task"], 'deadline': deadline}
        with open('tasks.json', 'r', encoding='utf-8') as rf:
            json_file = json.load(rf)
        with open('tasks.json', 'w', encoding='utf-8') as wf:
            for json_dict in json_file:
                if json_dict['tg_id'] == message.from_user.id:
                    json_dict['tasks'].append(task_dict)
                    json.dump(json_file, wf, ensure_ascii=False, indent=2)
                    break
        add_task_text = f'<b>Готово, добавлена задача:\n</b>' \
                        f'{data["task"]}\n' \
                        f'Срок до: {"Не указано" if message.text.lower() == "нет" else message.text}'
        await bot.send_message(message.chat.id, add_task_text, parse_mode="html", reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def incorrect_deadline(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    error_text = 'Нужно указывать дату в формате "DD-MM-YYYY", ' \
                 'либо ты указал неверную дату, попробуй ещё раз или напиши "Нет"'
    await bot.send_message(message.chat.id, error_text, parse_mode='html', reply_markup=markup)
