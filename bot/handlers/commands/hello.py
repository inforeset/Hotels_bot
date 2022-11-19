from telebot import TeleBot, types
from telebot.custom_filters import TextFilter

from bot.utils.misc.send_sticker import send_stickers


def start(message: types.Message, bot: TeleBot) -> None:
    """
    Handler works with start messages
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    send_stickers(bot=bot, chat_id=message.chat.id, sticker='hello')
    bot.send_message(chat_id=message.chat.id, text="Привет, для получения списка команд набери /help")


def register_start(bot: TeleBot) -> None:
    bot.register_message_handler(start,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 text=TextFilter(contains=("привет", "/hello-world", "/start"), ignore_case=True),
                                 states=None)
