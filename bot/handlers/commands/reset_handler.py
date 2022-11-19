from telebot import TeleBot
from telebot.types import Message

from bot.utils.main_functions.reset_all import reset


def reset_all(message: Message, bot: TeleBot) -> None:
    """
    For reset command, finist states and send users main menu
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    reset(bot=bot, message=message)


def register_reset_all(bot: TeleBot) -> None:
    bot.register_message_handler(reset_all,
                                 pass_bot=True,
                                 content_types=['text'],
                                 is_private=True,
                                 commands=['reset'],
                                 state='*')
