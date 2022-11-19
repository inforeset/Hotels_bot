from telebot import types, TeleBot

from bot.states.states import HotelsStates


def get_price_min_wrong(message: types.Message, bot: TeleBot) -> None:
    """
     Work with wrong min price messages from user
     :param message: Message
     :param bot: TeleBot
     :return: None
     """
    bot.send_message(chat_id=message.chat.id, text="Некорректный ввод, введите минимальную цену (руб/сут)")
    return


def register_get_price_min_wrong(bot: TeleBot) -> None:
    bot.register_message_handler(get_price_min_wrong,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.price_min,
                                 is_digit=False)
