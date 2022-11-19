from typing import Dict, Tuple, List, Union

from sqlalchemy.orm import Session

from bot.api.get_hotels import request_hotels
from bot.api.get_photo import request_photo
from bot.config_data.config_reader import Config
from bot.utils.db.check_photo import photo_exist


def photo_and_hotels(data: Dict, config: Config, session: Session) -> \
        Union[Tuple[List[Dict], List[Dict]], Tuple[None, None]]:
    """
    Main function for getting hotels and photo from api
    :param data: Dict
    :param config: Config
    :param session: Session
    :return: Tuple[List[Dict], List[Dict]]
    """
    photos = []
    hotels = request_hotels(data=data, config=config)
    if hotels:
        for hotel in hotels:
            if not data['quantity_photo']:
                break
            if not photo_exist(hotel_id=hotel['hotel_id'], session=session):
                request_p = request_photo(id_hotel=hotel['hotel_id'], config=config)
                if request_p:
                    photos.extend(request_p)
        return hotels, photos
    return None, None
