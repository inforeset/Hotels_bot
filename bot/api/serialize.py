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
            adress = f'{hotel["address"]["countryName"]}, {data["city"].capitalize()}, {hotel["address"].get("postalCode", "")}, {hotel["address"].get("streetAddress", "")}'
            if len(hotel['landmarks']):
                if hotel['landmarks'][0]['label'] == 'Центр города':
                    center = float(hotel['landmarks'][0]['distance'].split()[0].replace(',', '.'))
            price = float(hotel.get('ratePlan', {}).get('price', {}).get('exactCurrent', 0))
            coordinates = f"{hotel['coordinate'].get('lat', 0)},{hotel['coordinate'].get('lon', 0)}"
            star_rating = int(hotel['starRating'])
            user_rating = float(hotel.get('guestReviews', {}).get('rating', '0,0').replace(',', '.'))
            distance = data.get('distance')
            if distance and distance < center:
                return hotels
            hotels.append({'hotel_id': hotel_id,
                           'name': name,
                           'adress': adress,
                           'center': center,
                           'price': price,
                           'coordinates': coordinates,
                           'star_rating': star_rating,
                           'user_rating': user_rating})
        except (LookupError, ValueError) as exc:
            logger.error(exc, exc_info=exc)
            continue
    return hotels