import datetime
from typing import Dict

from sqlalchemy.orm import Session

from bot.database.models import History


def set_history(data: Dict, error: bool, session: Session) -> History:
    """
    Write history to db
    :param data: Dict
    :param error: bool
    :param session: Session
    :return: History
    """
    record_h = History()
    record_h.telegram_id = data['telegram_id']
    record_h.check_in = datetime.datetime.strptime(data['check_in'], '%Y-%m-%d')
    record_h.check_out = datetime.datetime.strptime(data['check_out'], '%Y-%m-%d')
    record_h.city = data['city']
    record_h.command = data['command']
    record_h.date_time = datetime.datetime.strptime(data['date_time'], '%d.%m.%Y %H:%M:%S')
    record_h.error = error
    record_h.period = data['period']
    record_h.quantity_display = data['quantity_display']
    record_h.quantity_photo = data['quantity_photo']
    if data['command'] == '/bestdeal':
        record_h.distance = data['distance']
        record_h.price_max = data['price_max']
        record_h.price_min = data['price_min']
    session.add(record_h)
    session.flush()
    return record_h
