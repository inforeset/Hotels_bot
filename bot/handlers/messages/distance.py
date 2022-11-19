from telebot import types, TeleBot

from bot.keyboards.inline.photo_kb import get_photo_kb
from bot.states.states import HotelsStates


def get_distance(message: types.Message, bot: TeleBot) -> None:
    """
    Get distance from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    text = int(message.text)
    if int(message.text) == 0:
        text = 1
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance'] = text
    bot.send_message(chat_id=message.chat.id, text="Будем загружать фотографии?", reply_markup=get_photo_kb())
    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=HotelsStates.photo)


def register_get_distance(bot: TeleBot) -> None:
    bot.register_message_handler(get_distance,
                                 pass_bot=True,
                                 content_types=['text'],
                                 is_private=True,
                                 state=HotelsStates.distance,
                                 is_digit=True)
