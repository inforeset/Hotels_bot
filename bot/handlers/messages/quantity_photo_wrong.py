from telebot import types, TeleBot

from bot.config_data.config_reader import Config
from bot.states.states import HotelsStates


def get_quantity_photo_wrong(message: types.Message, bot: TeleBot, config: Config) -> None:
    """
     Work with wrong quantity photo messages from user
     :param message: Message
     :param bot: TeleBot
     :return: None
     """
    bot.send_message(chat_id=message.chat.id,
                     text=f"Некорректный ввод, введите кол-во фотографий ({config.rapid_api.max_photo})")
    return


def register_get_quantity_photo_wrong(bot: TeleBot) -> None:
    bot.register_message_handler(get_quantity_photo_wrong,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.quantity_photo)
