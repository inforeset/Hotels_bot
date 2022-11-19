from sqlalchemy.orm import Session
from telebot import TeleBot, types

from bot.config_data.config_reader import Config
from bot.states.states import HotelsStates
from bot.utils.main_functions.finish import final


def get_quantity_photo(message: types.Message, bot: TeleBot, config: Config, session: Session) -> None:
    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=HotelsStates.final)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity_photo'] = int(message.text)
    final(bot=bot, message=message, config=config, session=session)


def register_get_quantity_photo(bot: TeleBot):
    bot.register_message_handler(get_quantity_photo,
                                 pass_bot=True,
                                 is_private=True,
                                 content_types=['text'],
                                 state=HotelsStates.quantity_photo,
                                 in_range=5)
