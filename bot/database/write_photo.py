from typing import Dict, List

from sqlalchemy.orm import Session

from bot.database.models import Photo


def set_photo(photo: List[Dict], session: Session) -> None:
    """
    Write photo to db
    :param photo: List[Dict]
    :param session: Session
    :return: None
    """
    for one_photo in photo:
        record_photo = Photo()
        record_photo.hotel_id = one_photo['id_hotel']
        record_photo.photo = one_photo['url']
        session.add(record_photo)
