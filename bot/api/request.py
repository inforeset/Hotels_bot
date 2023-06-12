import logging
from typing import Dict

import requests
from lxml import etree
from requests import Response, request

from bot.config_data.config_reader import Config

logger = logging.getLogger(__name__)

def get_request(url: str, config: Config, method: str, payload: dict = None, params: Dict = None) -> Response:
    """
    Common function for making request to api, return response
    :param payload:
    :param method:
    :param url: str
    :param params: Dict
    :param config: Config
    :return: Response
    """
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.rapid_api.rapid_api_key
    }
    if payload:
        headers["Content-Type"] = "application/json"

    try:
        return request(method=method, json=payload, url=url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as exc:
        logger.error(exc, exc_info=exc)


def get_course() -> float:
    try:
        req = requests.get('https://www.cbr-xml-daily.ru/daily.xml', verify=False, timeout=5)
        parsed_body = etree.fromstring(req.content)
        return float(parsed_body.xpath('//Valute[@ID="R01235"]/Value/text()')[0].replace(',', '.'))
    except requests.exceptions.RequestException as exc:
        logger.error(exc, exc_info=exc)
        return 0