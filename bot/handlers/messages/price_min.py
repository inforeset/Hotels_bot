from telebot import types, TeleBot

from bot.states.states import HotelsStates


def get_price_min(message: types.Message, bot: TeleBot) -> None:
    """
    Get min price from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    text = int(message.text)
    if int(message.text) == 0:
        text = 1
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_min'] = text
    bot.send_message(chat_id=message.chat.id, text="Введите максимальную цену (руб/сут)")
    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=HotelsStates.price_max)


def register_get_price_min(bot: TeleBot) -> None:
    bot.register_message_handler(get_price_min,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.price_min,
                                 is_digit=True)
