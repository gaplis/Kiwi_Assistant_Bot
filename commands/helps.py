from telebot.async_telebot import AsyncTeleBot, types
from utils.markups import main_menu_markup


async def helps(message: types.Message, bot: AsyncTeleBot):
    help_text = f'<b>Тут ты можешь посмотреть, что я умею 😊</b>\n\n' \
                f'Можно воспользоваться клавиатурой, ' \
                f'но также ты можешь использовать команды, отправляя мне сообщения:\n' \
                f'<b>"Главное меню"</b> - открывает главное меню\n' \
                f'<b>"Профиль"</b> - открывает твой профиль\n' \
                f'<b>"Поменять имя"</b> - активирует смену твоего имени\n' \
                f'<b>"Указать город"</b> - активирует смену твоего города\n' \
                f'<b>"Ежедневник"</b> - показывает твои задачи\n' \
                f'<b>"Добавить задачу"</b> - активирует добавление задачи\n' \
                f'<b>"Изменить задачу"</b> - активирует изменение задачи\n' \
                f'<b>"Удалить задачу"</b> - активирует удаление задачи\n' \
                f'<b>"Погода"</b> - показывает погоду в твоём городе\n' \
                f'<b>"Погода ..город.."</b> - показывает погоду в городе, который ты указал после команды "Погода"\n' \
                f'<b>"Погода на 5 дней"</b> - показывает погоду в твоём городе на 5 дней вперёд\n' \
                f'<b>"Поиск"</b> - активирует поиск в Google\n' \
                f'<b>"Игры"</b> - открывает меню игр и твоей статистики\n' \
                f'<b>"Статистика"</b> - открывает статистику твоих игр\n' \
                f'<b>"Крестики-нолики"</b> - активирует начало игры "Крестики-нолики"\n' \
                f'<b>"Вордли"</b> - активирует начало игры "Вордли"\n' \
                f'<b>"Включить утренние уведомления"</b> - включает утренние уведомления"\n' \
                f'<b>"Выключить утренние уведомления"</b> - выключает утренние уведомления"\n' \
                f'<b>"Включить уведомления о задачах"</b> - включает уведомления о дедлайнах задач ' \
                f'(сегодня, за 1 день, за 3 дня, за 7 дней)"\n' \
                f'<b>"Выключить уведомления о задачах"</b> - выключает уведомления о дедлайнах задач"\n' \

    await bot.send_message(message.from_user.id, help_text, reply_markup=main_menu_markup())