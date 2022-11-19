from telebot import TeleBot
from telebot.types import Message

from bot.api.request_cities import request_city
from bot.config_data.config_reader import Config
from bot.keyboards.inline.cities_kb import cities_keyboard
from bot.states.states import HotelsStates
from bot.utils.main_functions.reset_all import reset
from bot.utils.misc.send_sticker import send_stickers


def city(message: Message, bot: TeleBot, config: Config) -> None:
    """
    Send a request to api to get list of cities, and send Inline keyboard with founded cities
    :param message: Message
    :param bot: TeleBot
    :param config: Config
    :return: None
    """
    load = send_stickers(bot=bot, chat_id=message.chat.id, sticker='load_city')
    cities = request_city(city=message.text, config=config)
    if cities:
        bot.set_state(user_id=message.from_user.id, state=HotelsStates.enter_city, chat_id=message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['cities'] = cities
        bot.delete_message(message_id=load.id, chat_id=message.chat.id)
        bot.send_message(chat_id=load.chat.id,
                         text='Вот что удалось найти:',
                         reply_markup=cities_keyboard(cities))
    else:
        bot.edit_message_text(message_id=load.id, chat_id=load.chat.id, text="Ничего не нашлось!")
        reset(bot=bot, message=message)


def register_city(bot: TeleBot) -> None:
    bot.register_message_handler(city,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.start)
