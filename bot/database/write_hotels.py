from typing import Dict, List

from sqlalchemy.orm import Session

from bot.database.models import History, Hotels


def set_hotels(hotels: List[Dict], record_history: History, session: Session) -> List[Hotels]:
    """
    Write hotels to db
    :param hotels: List[Dict]
    :param record_history: History
    :param session: Session
    :return: -> List[Hotels]
    """
    writed_hotels = []
    for hotel in hotels:
        record_hot = Hotels()
        record_hot.history_id = record_history.record_id
        record_hot.hotel_id = hotel['hotel_id']
        record_hot.center = hotel['center']
        record_hot.coordinates = hotel['coordinates']
        record_hot.adress = hotel['adress']
        record_hot.name = hotel['name']
        record_hot.price = hotel['price']
        record_hot.star_rates = hotel['star_rating']
        record_hot.user_rates = hotel['user_rating']
        session.add(record_hot)
        writed_hotels.append(record_hot)
    return writed_hotels
