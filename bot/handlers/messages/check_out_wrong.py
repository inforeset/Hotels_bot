from telebot import types, TeleBot

from bot.states.states import HotelsStates


def get_check_out_wrong(message: types.Message, bot: TeleBot) -> None:
    """
    Work with wrong check out messages from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="Ошибка, введите цифрами кол-во дней (максимум 60)")
    return


def register_check_out_wrong(bot: TeleBot) -> None:
    bot.register_message_handler(get_check_out_wrong,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.check_out)
