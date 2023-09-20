from telebot.async_telebot import types
from utils.states import ChangeTaskStates
import json


async def change_task(message, bot):
    with open('tasks.json', 'r', encoding='utf-8') as rf:
        json_file = json.load(rf)
    for json_dict in json_file:
        if json_dict['tg_id'] == message.from_user.id:
            tasks_list = json_dict['tasks']
            if tasks_list:
                get_task_id_text = 'Напиши номер задачи, которую хочешь изменить:\n'
                for i, item in enumerate(tasks_list, start=1):
                    get_task_id_text += f'{i}: {item["task"]}\n'

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                cancel_button = types.InlineKeyboardButton('Отмена')
                markup.row(cancel_button)

                await bot.set_state(message.from_user.id, ChangeTaskStates.id_task, message.chat.id)
                return await bot.send_message(message.chat.id, get_task_id_text, parse_mode='html', reply_markup=markup)
    else:
        tasks_not_found_text = 'У тебя нет активных задач.\n' \
                               'Ты можешь вернуться и добавить ее'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu_button = types.InlineKeyboardButton('Главное меню')
        markup.row(main_menu_button)

        await bot.send_message(message.chat.id, tasks_not_found_text, parse_mode='html', reply_markup=markup)


async def cancel_change_task(message, bot):
    cancel_text = "Может, так даже лучше 😁"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    await bot.send_message(message.chat.id, cancel_text, parse_mode='html', reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def get_task_id(message, bot):
    get_new_data_text = 'А теперь напиши изменённую задачу'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    await bot.send_message(message.chat.id, get_new_data_text, parse_mode='html', reply_markup=markup)
    await bot.set_state(message.from_user.id, ChangeTaskStates.new_data, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id_task'] = message.text


async def incorrect_task_id(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.InlineKeyboardButton('Отмена')
    markup.row(cancel_button)

    error_text = 'Похоже, ты указал задачу, которой нет, или написал не число.\n' \
                 'Попробуй снова, ты должен ввести номер задачи'
    await bot.send_message(message.chat.id, error_text, parse_mode='html', reply_markup=markup)


async def get_new_data(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton('Главное меню')
    markup.row(main_menu_button)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        with open('tasks.json', 'r', encoding='utf-8') as rf:
            json_file = json.load(rf)
        with open('tasks.json', 'w', encoding='utf-8') as wf:
            for json_dict in json_file:
                if json_dict['tg_id'] == message.from_user.id:
                    json_dict['tasks'][int(data['id_task']) - 1]['task'] = message.text
                    json.dump(json_file, wf, ensure_ascii=False, indent=2)
                    break
        add_task_text = f'<b>Готово, изменена задача {data["id_task"]}:\n</b>' \
                        f'{message.text}\n'
        await bot.send_message(message.chat.id, add_task_text, parse_mode="html", reply_markup=markup)
    await bot.delete_state(message.from_user.id, message.chat.id)
