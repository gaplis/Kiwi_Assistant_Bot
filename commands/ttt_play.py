from random import choice

from telebot.async_telebot import AsyncTeleBot

from utils.states import TTTGameState
from utils.db import DataBase
from utils.markups import main_menu_markup, ttt_play_markup
from utils.ttt_engine import rand_choice_bot_in_ttt_game, check_win


async def ttt_game(message, bot):
    ttt_game_text = f'<b>ПРАВИЛА ИГРЫ "КРЕСТИКИ-НОЛИКИ"</b>\n\n' \
                    f'Игроки по очереди ставят на свободные клетки поля 3×3 знаки ' \
                    f'(один всегда крестики, другой всегда нолики)\n' \
                    f'Первый, выстроивший в ряд 3 своих фигуры по вертикали, ' \
                    f'горизонтали или большой диагонали, выигрывает\n' \
                    f'Если игроки заполнили все 9 ячеек и оказалось, что ни в одной вертикали, горизонтали или ' \
                    f'большой диагонали нет трёх одинаковых знаков, партия считается закончившейся в ничью\n' \
                    f'Первый ход делает игрок, ставящий крестики\n'

    await bot.set_state(message.from_user.id, TTTGameState.game, message.chat.id)
    await bot.send_message(message.chat.id, ttt_game_text)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['field'] = [[None for _ in range(3)] for _ in range(3)]
        data['players'] = {'player': None, 'cpu': None}
        data['first_step'] = choice(['player', 'cpu'])
        data['now_step'] = data['first_step']

        bot_step = None
        if data['first_step'] == 'player':
            data['players']['player'] = '❌'
            data['players']['cpu'] = '🟢'
            start_game_text = f'Первым ходишь ты, начали!'

            step_text = f''
            for i in data['field']:
                for j in i:
                    step_text += f'{j if j is not None else "⬛️"}'
                step_text += '\n'

        else:
            data['players']['cpu'] = '❌'
            data['players']['player'] = '🟢'
            data['field'] = rand_choice_bot_in_ttt_game(data['field'], data['players']['cpu'])

            start_game_text = f'Первой хожу я, начали!'

            step_text = f''
            for i in data['field']:
                for j in i:
                    step_text += f'{j if j is not None else "⬛️"}'
                step_text += '\n'

            data['now_step'] = 'player'
            bot_step = f'Теперь твой ход'

        await bot.send_message(message.chat.id, start_game_text)
        await bot.send_message(message.chat.id, step_text, reply_markup=ttt_play_markup(data['field']))
        if bot_step is not None:
            await bot.send_message(message.chat.id, bot_step, reply_markup=ttt_play_markup(data['field']))


async def cancel_ttt_game(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.U_ID)
        user_id = cursor.fetchone()[0]
        db.find_statistics(user_id, db.LEAVES['TTT'])
        leaves = cursor.fetchone()[0]
        db.update_statistics(user_id, db.LEAVES['TTT'], leaves + 1)

    cancel_text = "А ты ведь мог выиграть..."

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def play_ttt_game(message, bot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        buttons = {
            '↖️': {'res': data['field'][0][0], 'i': 0, 'j': 0},
            '⬆️': {'res': data['field'][0][1], 'i': 0, 'j': 1},
            '↗️': {'res': data['field'][0][2], 'i': 0, 'j': 2},
            '⬅️': {'res': data['field'][1][0], 'i': 1, 'j': 0},
            '⏺': {'res': data['field'][1][1], 'i': 1, 'j': 1},
            '➡️': {'res': data['field'][1][2], 'i': 1, 'j': 2},
            '↙️': {'res': data['field'][2][0], 'i': 2, 'j': 0},
            '⬇️': {'res': data['field'][2][1], 'i': 2, 'j': 1},
            '↘️': {'res': data['field'][2][2], 'i': 2, 'j': 2},
        }

        if message.text in '️❌🟢':
            busy_place_text = f'Это поле уже занято, выбери другое'

            return await bot.send_message(message.chat.id, busy_place_text,
                                          reply_markup=ttt_play_markup(data['field']))

        if message.text not in buttons:
            missing_button_text = f'Похоже, ты отправил что-то не то\n' \
                                  f'Попробуй воспользоваться клавиатурой снизу'

            return await bot.send_message(message.chat.id, missing_button_text,
                                          reply_markup=ttt_play_markup(data['field']))

        i = buttons[message.text]['i']
        j = buttons[message.text]['j']
        data['field'][i][j] = data['players']['player']

        step_text = f''
        for i in data['field']:
            for j in i:
                step_text += f'{j if j is not None else "⬛️"}'
            step_text += '\n'

        win_player = check_win(data['field'], data['players']['player'], data['now_step'])
        if win_player is None:
            await bot.send_message(message.chat.id, step_text)
            data['now_step'] = 'cpu'
        elif win_player is data['now_step']:
            db = DataBase()
            with db as cursor:
                db.find_user(message.from_user.id, db.U_ID)
                user_id = cursor.fetchone()[0]
                db.find_statistics(user_id, db.WINS['TTT'])
                wins = cursor.fetchone()[0]
                db.update_statistics(user_id, db.WINS['TTT'], wins + 1)

            win_player_text = f'Ты выиграл, поздровляю!'

            await bot.send_message(message.chat.id, step_text)
            await bot.send_message(message.chat.id, win_player_text, reply_markup=main_menu_markup())
            return await bot.delete_state(message.from_user.id, message.chat.id)
        else:
            db = DataBase()
            with db as cursor:
                db.find_user(message.from_user.id, db.U_ID)
                user_id = cursor.fetchone()[0]
                db.find_statistics(user_id, db.DRAWS['TTT'])
                draws = cursor.fetchone()[0]
                db.update_statistics(user_id, db.DRAWS['TTT'], draws + 1)

            draw_text = f'Похоже, у нас ничья 😄'

            await bot.send_message(message.chat.id, step_text)
            await bot.send_message(message.chat.id, draw_text, reply_markup=main_menu_markup())
            return await bot.delete_state(message.from_user.id, message.chat.id)

        bot_walks_text = f'Теперь мой ход'

        await bot.send_message(message.chat.id, bot_walks_text)
        data['field'] = rand_choice_bot_in_ttt_game(data['field'], data['players']['cpu'])

        step_text = f''
        for i in data['field']:
            for j in i:
                step_text += f'{j if j is not None else "⬛️"}'
            step_text += '\n'

        win_cpu = check_win(data['field'], data['players']['cpu'], data['now_step'])
        if win_cpu is None:
            await bot.send_message(message.chat.id, step_text)
            data['now_step'] = 'player'
        elif win_cpu is data['now_step']:
            db = DataBase()
            with db as cursor:
                db.find_user(message.from_user.id, db.U_ID)
                user_id = cursor.fetchone()[0]
                db.find_statistics(user_id, db.LOSES['TTT'])
                loses = cursor.fetchone()[0]
                db.update_statistics(user_id, db.LOSES['TTT'], loses + 1)

            win_player_text = f'Я выиграл! ☺️'

            await bot.send_message(message.chat.id, step_text)
            await bot.send_message(message.chat.id, win_player_text, reply_markup=main_menu_markup())
            return await bot.delete_state(message.from_user.id, message.chat.id)
        else:
            db = DataBase()
            with db as cursor:
                db.find_user(message.from_user.id, db.U_ID)
                user_id = cursor.fetchone()[0]
                db.find_statistics(user_id, db.DRAWS['TTT'])
                draws = cursor.fetchone()[0]
                db.update_statistics(user_id, db.DRAWS['TTT'], draws + 1)

            draw_text = f'Похоже, у нас ничья 😄'

            await bot.send_message(message.chat.id, step_text)
            await bot.send_message(message.chat.id, draw_text, reply_markup=main_menu_markup())
            return await bot.delete_state(message.from_user.id, message.chat.id)

        player_walks_text = f'Теперь твой ход'
        await bot.send_message(message.chat.id, player_walks_text, reply_markup=ttt_play_markup(data['field']))


def route(bot: AsyncTeleBot):
    bot.register_message_handler(ttt_game, ttt_game_commands=True, pass_bot=True)
    bot.register_message_handler(cancel_ttt_game, state=TTTGameState.game, give_up_commands=True, pass_bot=True)
    bot.register_message_handler(play_ttt_game, state=TTTGameState.game, pass_bot=True)
