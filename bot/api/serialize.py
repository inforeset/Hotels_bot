import logging
from typing import Dict, List


def parse_result(parse_list: List, data: Dict) -> List[Dict]:
    """
    Prepare data from api for loading to db
    :param parse_list: List
    :param data: Dict
    :return: List[Dict]
    """
    hotels = []
    hotel_id, name, address, center, price = '', '', '', 'нет данных', ''
    logger = logging.getLogger(__name__)

    for hotel in parse_list:
        try:
            hotel_id = int(hotel['id'])
            name = hotel['name']
            adress = ''
            center = float(hotel['destinationInfo']['distanceFromDestination']['value']) * 1.61
            price = float(hotel['price']['lead']['amount'])
            if data['ue']:
                price *= data['ue']
            coordinates = f"0,0"
            star_rating = hotel.get('star')
            if star_rating:
                star_rating = int(star_rating)
            else:
                star_rating = 0
            user_rating = float(hotel['reviews']['total'])
            distance = data.get('distance')
            if distance and distance < center:
                return hotels
            hotels.append(
                {
                    'hotel_id': hotel_id,
                    'name': name,
                    'adress': adress,
                    'center': center,
                    'price': price,
                    'coordinates': coordinates,
                    'star_rating': star_rating,
                    'user_rating': user_rating
                }
            )
        except (LookupError, ValueError) as exc:
            logger.error(exc, exc_info=exc)
            continue
    return hotels
