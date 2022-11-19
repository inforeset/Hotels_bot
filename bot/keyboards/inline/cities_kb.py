from typing import Dict

from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

cities_factory = CallbackData('city_id', prefix='city')


def cities_keyboard(cities: Dict) -> InlineKeyboardMarkup:
    """
    Return InlineKeyboardMarkup for founded cities
    :param cities: Dict
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text=city['caption'],
                    callback_data=cities_factory.new(city_id=destination_id)
                )
            ]
            for destination_id, city in cities.items()
        ]
    )
