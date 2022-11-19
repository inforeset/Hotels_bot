import logging

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import Message


def send_stickers(bot: TeleBot, chat_id: int, sticker: str) -> Message:
    """
    For sending stickers to chat
    :param bot: TeleBot
    :param chat_id: int
    :param sticker: str
    :return: Message
    """
    logger = logging.getLogger(__name__)
    stickers = {
        'hello': 'CAACAgIAAxkBAAIkSmNw7R2QJP6T3eGbvKoqsES0EK0tAALRVAACns4LAAG8xxX5XML5qCsE',
        'load_city': 'CAACAgIAAxkBAAIkTGNw7hCsQjcpmCIsvlqDo3CZbC8aAALUVAACns4LAAEkxTcvOBTIZisE',
        'load_hotels': 'CAACAgIAAxkBAAIfXGNqV3rLvW1fjlV1GB9RHvaCYwXXAALkVAACns4LAAELthoS7W5HeysE'
    }
    try:
        load = bot.send_sticker(chat_id=chat_id, protect_content=True,
                                sticker=stickers[sticker])
    except ApiTelegramException as exc:
        logger.exception(exc)
        load = bot.send_message(chat_id=chat_id, text='Ищем...')
    return load
