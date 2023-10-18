from utils.db import DataBase
from utils.markups import main_menu_markup


async def statistics(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.U_ID)
        user_id = cursor.fetchone()[0]
        db.find_statistics(user_id, f"{db.WINS['TTT']}, {db.LOSES['TTT']}, {db.DRAWS['TTT']}, {db.LEAVES['TTT']}, "
                                    f"{db.WINS['WORDLE']}, {db.LOSES['WORDLE']}, {db.LEAVES['WORDLE']}")
        stats = cursor.fetchone()

    ttt_wins = stats[0]
    ttt_loses = stats[1]
    ttt_draws = stats[2]
    ttt_leaves = stats[3]
    wordle_wins = stats[4]
    wordle_loses = stats[5]
    wordle_leaves = stats[6]

    statistics_text = f'Твоя статистика\n\n'

    ttt_all_plays = ttt_wins + ttt_loses + ttt_draws + ttt_leaves
    ttt_finally_plays = ttt_wins + ttt_loses + ttt_draws
    if ttt_all_plays != 0:
        statistics_text += f'<b>Крестики-нолики</b>\n' \
                           f'Всего игр: <b>{ttt_all_plays}</b>\n' \
                           f'Побед: <b>{ttt_wins}</b>'
        if ttt_finally_plays != 0:
            statistics_text += f', % от законченных игр: <b>{(ttt_wins / ttt_finally_plays * 100):.2f}%</b>\n'
        else:
            statistics_text += '\n'
        statistics_text += f'Поражений: <b>{ttt_loses}</b>'
        if ttt_finally_plays != 0:
            statistics_text += f', % от законченных игр: <b>{(ttt_loses / ttt_finally_plays * 100):.2f}%</b>\n'
        else:
            statistics_text += '\n'
        statistics_text += f'Ничьей: <b>{ttt_draws}</b>'
        if ttt_finally_plays != 0:
            statistics_text += f', % от законченных игр: <b>{(ttt_draws / ttt_finally_plays * 100):.2f}%</b>\n\n'
        else:
            statistics_text += '\n\n'
        statistics_text += f'Законченных игр: <b>{ttt_finally_plays}</b>, ' \
                           f'% от всех игр: <b>{(ttt_finally_plays / ttt_all_plays * 100):.2f}%</b>\n' \
                           f'Покинутых игр: <b>{ttt_leaves}</b>, ' \
                           f'% от всех игр: <b>{(ttt_leaves / ttt_all_plays * 100):.2f}%</b>\n\n'

    wordle_all_plays = wordle_wins + wordle_loses + wordle_leaves
    wordle_finally_plays = wordle_wins + wordle_loses
    if wordle_all_plays != 0:
        statistics_text += f'<b>Вордли</b>\n' \
                           f'Всего игр: <b>{wordle_all_plays}</b>\n' \
                           f'Побед: <b>{wordle_wins}</b>'
        if wordle_finally_plays != 0:
            statistics_text += f', % от законченных игр: <b>{(wordle_wins / wordle_finally_plays * 100):.2f}%</b>\n'
        else:
            statistics_text += '\n'
        statistics_text += f'Поражений: <b>{wordle_loses}</b>'
        if wordle_finally_plays != 0:
            statistics_text += f', % от законченных игр: <b>{(wordle_loses / wordle_finally_plays * 100):.2f}%</b>\n\n'
        else:
            statistics_text += '\n\n'
        statistics_text += f'Законченных игр: <b>{wordle_finally_plays}</b>, ' \
                           f'% от всех игр: <b>{(wordle_finally_plays / wordle_all_plays * 100):.2f}%</b>\n' \
                           f'Покинутых игр: <b>{wordle_leaves}</b>, ' \
                           f'% от всех игр: <b>{(wordle_leaves / wordle_all_plays * 100):.2f}%</b>\n\n'

    if statistics_text == 'Твоя статистика\n\n':
        statistics_text = 'Ты пока еще ни во что не играл, попробуй!'

    await bot.send_message(message.from_user.id, statistics_text, reply_markup=main_menu_markup())
