from utils.states import WordleGameState
from utils.markups import cancel_markup, main_menu_markup
from utils.wordle_engine import get_random_word, get_text_with_emoji, checking_for_word_existence
from utils.db import DataBase


async def wordle_game(message, bot):
    wordle_game_text = f'<b>ПРАВИЛА ИГРЫ "ВОРДЛИ"</b>\n\n' \
                       f'Будет загадано слово из 6 букв и у тебя будет 6 попыток, чтобы его угадать\n' \
                       f'❌ - этой буквы нет в слове\n' \
                       f'⚠️ - буква в слове есть, но стоит не на своём месте\n' \
                       f'✅ - буква стоит на своём месте\n'

    start_game_text = 'Начали! Попытка №1'

    await bot.set_state(message.from_user.id, WordleGameState.game, message.chat.id)
    await bot.send_message(message.chat.id, wordle_game_text)
    await bot.send_message(message.chat.id, start_game_text, reply_markup=cancel_markup())
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = get_random_word()
        data['step'] = 1
        data['steps'] = {}


async def cancel_wordle_game(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.U_ID)
        user_id = cursor.fetchone()[0]
        db.find_statistics(user_id, db.LEAVES['WORDLE'])
        leaves = cursor.fetchone()[0]
        db.update_statistics(user_id, db.LEAVES['WORDLE'], leaves + 1)

    cancel_text = "Никогда не сдавайся!"

    await bot.send_message(message.chat.id, cancel_text, reply_markup=main_menu_markup())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def play_wordle_game(message, bot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for item in data['steps']:
            if message.text.lower() == data["steps"][item]["word"]:
                repeat_word_text = f'Ты уже проверял слово {message.text.upper()}, попробуй другое'

                return await bot.send_message(message.from_user.id, repeat_word_text, reply_markup=cancel_markup())
        if not checking_for_word_existence(message.text.lower()):
            not_found_word_text = f'Похоже, такого слова не существует.\n' \
                                  f'Пока что...'

            return await bot.send_message(message.from_user.id, not_found_word_text, reply_markup=cancel_markup())
        if data['step'] < 6:
            if message.text.lower() != data['word']:
                data['steps'][data['step']] = {'word': '', 'text': ''}
                data['steps'][data['step']]['word'] = message.text.lower()
                data['steps'][data['step']]['text'] = get_text_with_emoji(data['word'], message.text.lower())

                incorrect_word_text = f'Неверно:\n\n'
                for i, item in enumerate(data['steps'], start=1):
                    incorrect_word_text += f'{i}. {data["steps"][item]["text"]}\n\n'
                now_step_text = "Последняя попытка" if data["step"] + 1 == 6 else f'Попытка #{data["step"] + 1}'

                data['step'] += 1
                await bot.send_message(message.from_user.id, incorrect_word_text)
                await bot.send_message(message.from_user.id, now_step_text, reply_markup=cancel_markup())
            else:
                db = DataBase()
                with db as cursor:
                    db.find_user(message.from_user.id, db.U_ID)
                    user_id = cursor.fetchone()[0]
                    db.find_statistics(user_id, db.WINS['WORDLE'])
                    wins = cursor.fetchone()[0]
                    db.update_statistics(user_id, db.WINS['WORDLE'], wins + 1)

                win_text = f'Верно! Это было слово - {data["word"].upper()}'

                await bot.send_message(message.from_user.id, win_text, reply_markup=main_menu_markup())
                await bot.delete_state(message.from_user.id, message.chat.id)
        else:
            if message.text.lower() != data['word']:
                data['steps'][data['step']] = {'word': '', 'text': ''}
                data['steps'][data['step']]['word'] = message.text
                data['steps'][data['step']]['text'] = get_text_with_emoji(data['word'], message.text.lower())

                db = DataBase()
                with db as cursor:
                    db.find_user(message.from_user.id, db.U_ID)
                    user_id = cursor.fetchone()[0]
                    db.find_statistics(user_id, db.LOSES['WORDLE'])
                    loses = cursor.fetchone()[0]
                    db.update_statistics(user_id, db.LOSES['WORDLE'], loses + 1)

                lose_text = f'Увы, все попытки кончились 😢\n' \
                            f'Это было слово - {data["word"].upper()}\n\n'
                for i, item in enumerate(data['steps'], start=1):
                    lose_text += f'{i}. {data["steps"][item]["text"]}\n\n'

                await bot.send_message(message.from_user.id, lose_text, reply_markup=main_menu_markup())
                await bot.delete_state(message.from_user.id, message.chat.id)
            else:
                db = DataBase()
                with db as cursor:
                    db.find_user(message.from_user.id, db.U_ID)
                    user_id = cursor.fetchone()[0]
                    db.find_statistics(user_id, db.WINS['WORDLE'])
                    wins = cursor.fetchone()[0]
                    db.update_statistics(user_id, db.WINS['WORDLE'], wins + 1)

                win_text = f'Верно! Это было слово - {data["word"].upper()}'

                await bot.send_message(message.from_user.id, win_text, reply_markup=main_menu_markup())
                await bot.delete_state(message.from_user.id, message.chat.id)


async def incorrect_length_word(message, bot):
    error_text = 'Слово должно состоять из 6 букв, будь внимателен'

    await bot.send_message(message.chat.id, error_text, reply_markup=cancel_markup())
