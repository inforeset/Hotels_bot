import datetime
from uuid import uuid4

from telebot import TeleBot
from telebot.types import Message

from bot.api.request import get_course
from bot.states.states import HotelsStates


def commands_price(message: Message, bot: TeleBot) -> None:
    """
    For commands "lowprice", "highprice", "bestdeal"
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="В каком городе будем искать?")
    bot.set_state(user_id=message.from_user.id, state=HotelsStates.start, chat_id=message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        data['date_time'] = datetime.datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S')
        data['telegram_id'] = message.from_user.id
        data['chat_id'] = message.chat.id
        data['ue'] = get_course()


def register_commands_price(bot: TeleBot) -> None:
    bot.register_message_handler(commands_price,
                                 pass_bot=True,
                                 content_types=['text'],
                                 commands=["lowprice", "highprice", "bestdeal"],
                                 is_private=True,
                                 state=None)
