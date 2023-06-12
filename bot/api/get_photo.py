import json
import logging
from json import JSONDecodeError

from sqlalchemy.orm import Session

from bot.api.request import get_request
from bot.config_data.config_reader import Config
from bot.utils.db.check_photo import photo_exist


def request_photo(id_hotel: int, config: Config, session: Session) -> dict:
    """
    Make request to api for getting photo's urls
    :param id_hotel: str
    :param config: Config
    :return: List[Dict]
    """
    logger = logging.getLogger(__name__)
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    querystring = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": str(id_hotel)
    }
    try:
        response = get_request(url, payload=querystring, config=config, method="POST")
        if not response or response.status_code != 200:
            return {}
        data = json.loads(response.text)
        info = {"address": data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
                "coordinates": f"{data['data']['propertyInfo']['summary']['location']['coordinates']['latitude']},"
                               f"{data['data']['propertyInfo']['summary']['location']['coordinates']['longitude']}",
                'photos': []}

        if not photo_exist(hotel_id=str(id_hotel), session=session):
            for photo in data['data']['propertyInfo']['propertyGallery']['images']:
                url = photo['image']['url']
                info['photos'].append({'id_hotel': id_hotel, 'url': url})
        return info
    except (JSONDecodeError, TypeError) as exc:
        logger.error(exc, exc_info=exc)
