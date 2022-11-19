from telebot import TeleBot
from telebot.types import Message

from bot.utils.main_functions.help_func import help_message


def reset(bot: TeleBot, message: Message):
    bot.delete_state(chat_id=message.chat.id, user_id=message.from_user.id)
    help_message(bot=bot, message=message)