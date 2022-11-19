from telebot import TeleBot
from telebot.types import Message


def help_message(bot: TeleBot, message: Message) -> None:
    """
    Send menu to chat
    :param bot: TeleBot
    :param message: Message
    :return: None
    """
    bot.send_message(chat_id=message.chat.id, text="/lowprice — вывод самых дешёвых отелей в городе\n"
                                                   "/highprice — вывод самых дорогих отелей в городе\n"
                                                   "/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n"
                                                   "/history — вывод истории поиска отелей\n"
                                                   "/reset - выход в меню")
