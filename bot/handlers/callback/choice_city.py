from telebot import types, TeleBot

from bot.config_data.config_reader import Config
from bot.keyboards.inline.cities_kb import cities_factory
from bot.states.states import HotelsStates


def city_callback(call: types.CallbackQuery, bot: TeleBot, config: Config) -> None:
    """
    Callback write chosen city into storage and set next state
    :param call: CallbackQuery
    :param bot: TeleBot
    :param config: Config
    :return: None
    """
    callback_data: dict = cities_factory.parse(callback_data=call.data)
    city_id = callback_data['city_id']
    bot.set_state(user_id=call.from_user.id, state=HotelsStates.quantity, chat_id=call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        city = data['cities'][city_id]
        data['destination_id'] = city_id
        data['city'] = city['name']
        data['coordinates'] = f"{city['latitude']},{city['longitude']}"
        del data['cities']
    bot.edit_message_text(message_id=call.message.id,
                          chat_id=call.message.chat.id,
                          text=f"Какое количество отелей будем показывать (максимум {config.rapid_api.max_hotel})?",
                          reply_markup=None)


def register_city_callback(bot: TeleBot) -> None:
    bot.register_callback_query_handler(city_callback,
                                        func=None,
                                        pass_bot=True,
                                        config=cities_factory.filter(),
                                        state=HotelsStates.enter_city)
