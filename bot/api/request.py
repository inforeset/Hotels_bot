import logging
from typing import Dict

import requests
from requests import Response

from bot.config_data.config_reader import Config


def get_request(url: str, params: Dict, config: Config) -> Response:
    """
    Common function for making request to api, return response
    :param url: str
    :param params: Dict
    :param config: Config
    :return: Response
    """
    logger = logging.getLogger(__name__)
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.rapid_api.rapid_api_key
    }

    try:
        return requests.get(url=url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as exc:
        logger.error(exc, exc_info=exc)
