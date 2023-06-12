import json
import logging
from typing import Any, Dict

from bot.api.request import get_request
from bot.config_data.config_reader import Config
from bot.utils.request.clean_html import remove_span


def request_city(city: str, config: Config) -> Dict[Any, Dict[str, Any]]:
    """
    Get info about cities from api
    :param city:
    :param config:
    :return:
    """
    logger = logging.getLogger(__name__)
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": city, "locale": "ru_RU"}
    response = {}
    try:
        request = get_request(url=url, method="GET", config=config, params=querystring)
        if request.status_code != 200:
            raise LookupError(f'Status code {request.status_code}')
        if not request:
            return {}
        data = json.loads(request.text)
        if not data:
            raise LookupError('Response is empty')
        for entity in data["sr"]:
            if entity.get("gaiaId"):
                response[entity['gaiaId']] = {
                    'name': entity['regionNames']['shortName'],
                    'caption': entity['regionNames']['displayName'],
                    'latitude': entity['coordinates']['lat'],
                    'longitude': entity['coordinates']['long']
                }

        return response

    except (LookupError, TypeError) as exc:
        logger.error(exc, exc_info=exc)
