from telebot import types, TeleBot

from bot.states.states import HotelsStates


def get_price_max(message: types.Message, bot: TeleBot) -> None:
    """
    Get max price from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_max'] = int(message.text)
    bot.send_message(chat_id=message.chat.id, text="Введите максимальное расстояние от центра (км)")
    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=HotelsStates.distance)


def register_get_price_max(bot: TeleBot) -> None:
    bot.register_message_handler(get_price_max,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.price_max,
                                 price_max=True)
