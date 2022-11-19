from telebot import TeleBot
from telebot.types import Message

from bot.config_data.config_reader import Config
from bot.states.states import HotelsStates


def quantity_wrong(message: Message, bot: TeleBot, config: Config) -> None:
    """
     Work with wrong quantity hotels messages from user
     :param message: Message
     :param bot: TeleBot
     :return: None
     """
    bot.send_message(chat_id=message.chat.id,
                     text=f"Ошибка, повторите ввод. Какое количество отелей будем показывать ({config.rapid_api.max_hotel})?")
    return


def register_quantity_wrong(bot: TeleBot) -> None:
    bot.register_message_handler(quantity_wrong,
                                 pass_bot=True,
                                 content_types=['text'],
                                 state=HotelsStates.quantity,
                                 is_private=True)
