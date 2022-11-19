from telebot import types, TeleBot

from bot.states.states import HotelsStates


def get_distance_wrong(message: types.Message, bot: TeleBot) -> None:
    """
    Work with wrong distance messages from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="Некорректный ввод, введите максимальное расстояние от центра (км):")
    return


def register_get_distance_wrong(bot: TeleBot) -> None:
    bot.register_message_handler(get_distance_wrong,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.distance,
                                 is_digit=False)
