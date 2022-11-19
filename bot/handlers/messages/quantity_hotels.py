import datetime

from telebot import TeleBot
from telebot.types import Message

from bot.states.states import HotelsStates
from bot.utils.misc.calendar import MyStyleCalendar, LSTEP


def quantity(message: Message, bot: TeleBot) -> None:
    """
    Get quantity hotels from user
    :param message: Message
    :param bot: TeleBot
    :return: None
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity_display'] = int(message.text)
    bot.send_message(chat_id=message.chat.id, text="Планируемая дата заезда?")
    calendar, step = MyStyleCalendar(locale='ru', min_date=datetime.date.today()).build()
    bot.send_message(chat_id=message.chat.id, text=f"Выберите {LSTEP[step]}", reply_markup=calendar)
    bot.set_state(user_id=message.from_user.id, state=HotelsStates.check_in, chat_id=message.chat.id)


def register_quantity(bot: TeleBot) -> None:
    bot.register_message_handler(quantity,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.quantity,
                                 in_range=5)
