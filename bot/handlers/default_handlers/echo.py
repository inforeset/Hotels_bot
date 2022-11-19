from telebot import TeleBot
from telebot.types import Message


def bot_echo(message: Message, bot: TeleBot) -> None:
    """
    For unhandled messages
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="Я тебя не понимаю. Напиши /help.")


def register_echo(bot: TeleBot) -> None:
    bot.register_message_handler(bot_echo,
                                 pass_bot=True,
                                 is_private=True,
                                 state=None)
