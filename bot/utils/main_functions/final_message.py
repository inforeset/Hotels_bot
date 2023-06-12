import logging
from typing import Dict, List

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.apihelper import ApiException
from telebot.types import Message

from bot.database.get_photo_from_db import get_photo_db
from bot.database.models import Hotels
from bot.utils.misc.hotel_message import get_hotel_message
from bot.utils.misc.media_group import form_media_group


def result_message(hotels: List[Hotels], data: Dict, message: Message, bot: TeleBot, session: Session) -> None:
    """
    Form final messages with mediagroup and send it to chat
    :param hotels: List[Hotels]
    :param data: Dict
    :param message: Message
    :param bot: TeleBot
    :param session: Session
    :return: None
    """
    logger = logging.getLogger(__name__)
    for hotel in hotels:
        bot.send_message(chat_id=message.chat.id,
                         text=get_hotel_message(hotel=hotel, period=data['period'], data=data),
                         disable_web_page_preview=True)
        if data['quantity_photo']:
            photos_h = get_photo_db(session=session, hotel_id=hotel.hotel_id, limit=data['quantity_photo'])
            if photos_h:
                media = form_media_group(photos=photos_h)
                if len(media):
                    try:
                        bot.send_media_group(chat_id=message.chat.id, media=media)
                    except ApiException as exc:
                        logger.error(exc, exc_info=exc)
                        media = form_media_group(photos=photos_h, error=True)
                        if len(media):
                            bot.send_media_group(chat_id=message.chat.id, media=media)
                        else:
                            bot.send_message(chat_id=message.chat.id, text='Фотографии не найдены')
            else:
                bot.send_message(chat_id=message.chat.id, text='Фотографии не найдены')