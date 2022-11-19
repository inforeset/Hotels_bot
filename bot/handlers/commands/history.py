from sqlalchemy.orm import Session
from telebot import TeleBot, types

from bot.database.get_history_from_db import get_history_db
from bot.database.get_hotels_from_db import get_hotels_db
from bot.utils.main_functions.help_func import help_message
from bot.utils.misc.history_message import get_history_message
from bot.utils.misc.hotel_message import get_hotel_message


def get_history(message: types.Message, bot: TeleBot, session: Session) -> None:
    """
    For history command, get history from db ande send into chat
    :param message: Message
    :param bot: TeleBot
    :param session: Session
    :return: None
    """
    history = get_history_db(user_id=message.from_user.id, session=session)
    if not history:
        bot.send_message(chat_id=message.chat.id, text='Записей не найдено')
        help_message(bot=bot, message=message)
        return
    for record in history:
        bot.send_message(chat_id=message.chat.id,
                         text=get_history_message(record=record),
                         disable_web_page_preview=True)
        if record.error:
            bot.send_message(chat_id=message.chat.id, text='\nПри загрузке возникли ошибки, отели не загружены')
            help_message(bot=bot, message=message)
            return
        hotels = get_hotels_db(record_history=record, session=session)
        for hotel in hotels:
            bot.send_message(chat_id=message.chat.id,
                             text=get_hotel_message(hotel=hotel, period=record.period),
                             disable_web_page_preview=True)
    help_message(bot=bot, message=message)


def register_get_history(bot: TeleBot) -> None:
    bot.register_message_handler(get_history,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 commands=['history'],
                                 states=None)
