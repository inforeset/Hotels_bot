import datetime
import json
import logging
from json import JSONDecodeError
from typing import Dict, List

from bot.api.request import get_request
from bot.api.serialize import parse_result
from bot.config_data.config_reader import Config


def request_hotels(data: Dict, config: Config) -> List[Dict]:
    """
    Get a list of hotels from api and return it
    :param data: Dict
    :param config: Config
    :return: List
    """
    logger = logging.getLogger(__name__)
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    check_in = datetime.datetime.strptime(data['check_in'], '%Y-%m-%d')
    check_out = datetime.datetime.strptime(data['check_out'], '%Y-%m-%d')
    sort_order = ''
    price_min = ''
    price_max = ''
    page_size = data['quantity_display']
    if data['command'] == '/lowprice':
        sort_order = 'PRICE_LOW_TO_HIGH'
    elif data['command'] == '/highprice':
        sort_order = 'PRICE_LOW_TO_HIGH'
        page_size = 200
    elif data['command'] == '/bestdeal':
        sort_order = 'DISTANCE'
        price_min = data['price_min']
        price_max = data['price_max']

    payload = {
        "currency": "USD",
        "locale": "en_US",
        "destination": {"regionId": data['destination_id']},
        "checkInDate": {
            "day": check_in.day,
            "month": check_in.month,
            "year": check_in.year
        },
        "checkOutDate": {
            "day": check_out.day,
            "month": check_out.month,
            "year": check_out.year
        },
        "rooms": [
            {
                "adults": 1,
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": page_size,
        "sort": sort_order,
        "filters": {"price": {
            "max": price_max,
            "min": price_min
        }}
    }

    try:
        request = get_request(url=url, method='POST', payload=payload, config=config)
        if not request:
            return []
        data_request = json.loads(request.text)
        parsed = parse_result(parse_list=data_request['data']['propertySearch']['properties'], data=data)
        if data['command'] == '/highprice':
            return parsed[::-1][:data['quantity_display']]
        return parsed
    except (LookupError, JSONDecodeError, TypeError) as exc:
        logger.error(exc, exc_info=exc)
