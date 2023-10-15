from utils.db import DataBase
from utils.markups import main_menu_markup


async def statistics(message, bot):
    db = DataBase()
    with db as cursor:
        db.find_user(message.from_user.id, db.U_ID)
        user_id = cursor.fetchone()[0]
        db.find_statistics(user_id, f"{db.WINS['TTT']}, {db.LOSES['TTT']}, {db.LEAVES['TTT']}, "
                                    f"{db.WINS['WORDLE']}, {db.LOSES['WORDLE']}, {db.LEAVES['WORDLE']}")
        stats = cursor.fetchone()

    ttt_wins = stats[0]
    ttt_loses = stats[1]
    ttt_leaves = stats[2]
    wordle_wins = stats[3]
    wordle_loses = stats[4]
    wordle_leaves = stats[5]

    statistics_text = f'Твоя статистика\n\n'
    if ttt_wins != 0 or ttt_loses != 0 or ttt_leaves != 0:
        all_plays = ttt_wins + ttt_loses + ttt_leaves
        statistics_text += f'<b>Крестики-нолики</b>\n' \
                           f'Всего игр: <b>{all_plays}</b>\n' \
                           f'Побед: <b>{ttt_wins}</b>, ' \
                           f'% от законченных игр: <b>{(ttt_wins / (ttt_wins + ttt_loses) * 100):.2f}%</b>\n' \
                           f'Поражений: <b>{ttt_loses}</b>, ' \
                           f'% от законченных игр: <b>{(ttt_loses / (ttt_wins + ttt_loses) * 100):.2f}%</b>\n\n' \
                           f'Законченных игр: <b>{all_plays - ttt_leaves}</b>, ' \
                           f'% от всех игр: <b>{((all_plays - ttt_leaves) / all_plays * 100):.2f}%</b>\n' \
                           f'Покинутых игр: <b>{ttt_leaves}</b>, ' \
                           f'% от всех игр: <b>{(ttt_leaves / all_plays * 100):.2f}%</b>\n\n'

    if wordle_wins != 0 or wordle_loses != 0 or wordle_leaves != 0:
        all_plays = wordle_wins + wordle_loses + wordle_leaves
        statistics_text += f'<b>Вордли</b>\n' \
                           f'Всего игр: <b>{all_plays}</b>\n' \
                           f'Побед: <b>{wordle_wins}</b>, ' \
                           f'% от законченных игр: <b>{(wordle_wins / (wordle_wins + wordle_loses) * 100):.2f}%</b>\n' \
                           f'Поражений: <b>{wordle_loses}</b>, ' \
                           f'% от законченных игр: <b>{(wordle_loses / (wordle_wins + wordle_loses) * 100):.2f}%</b>\n\n' \
                           f'Законченных игр: <b>{all_plays - wordle_leaves}</b>, ' \
                           f'% от всех игр: <b>{((all_plays - wordle_leaves) / all_plays * 100):.2f}%</b>\n' \
                           f'Покинутых игр: <b>{wordle_leaves}</b>, ' \
                           f'% от всех игр: <b>{(wordle_leaves / all_plays * 100):.2f}%</b>\n\n'

    if statistics_text == 'Твоя статистика\n\n':
        statistics_text = 'Ты пока еще ни во что не играл, попробуй!'

    await bot.send_message(message.from_user.id, statistics_text, reply_markup=main_menu_markup())
