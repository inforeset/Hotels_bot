from sqlalchemy.orm import Session
from telebot import TeleBot, types
from telebot.custom_filters import TextFilter

from bot.config_data.config_reader import Config
from bot.states.states import HotelsStates


def no_photo(call: types.CallbackQuery, bot: TeleBot, config: Config, session: Session) -> None:
    """
    Callback if user choose not load photo
    :param call: CallbackQuery
    :param bot: TeleBot
    :param config: Config
    :param session: Session
    :return: None
    """
    bot.set_state(user_id=call.from_user.id, chat_id=call.message.chat.id, state=HotelsStates.final)
    bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
    final(bot=bot, message=call.message, config=config, session=session)


def register_no_photo_callback(bot: TeleBot) -> None:
    bot.register_callback_query_handler(no_photo,
                                        func=None,
                                        pass_bot=True,
                                        state=HotelsStates.photo,
                                        text=TextFilter(equals='no'))
