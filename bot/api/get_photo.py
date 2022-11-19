import json
import logging
from json import JSONDecodeError
from typing import List, Dict

from bot.api.request import get_request
from bot.config_data.config_reader import Config


def request_photo(id_hotel: int, config: Config) -> List[Dict]:
    """
    Make request to api for getting photo's urls
    :param id_hotel: str
    :param config: Config
    :return: List[Dict]
    """
    logger = logging.getLogger(__name__)
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    photos = []
    try:
        response = get_request(url, params=querystring, config=config)
        if not response:
            return []
        data = json.loads(response.text)
        for photo in data['hotelImages']:
            url = photo['baseUrl'].replace('_{size}', '_z')
            photos.append({'id_hotel': id_hotel, 'url': url})
        return photos
    except (JSONDecodeError, TypeError) as exc:
        logger.error(exc, exc_info=exc)