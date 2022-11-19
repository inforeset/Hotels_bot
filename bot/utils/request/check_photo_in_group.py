import logging

import requests


def check_foto(photo: str) -> bool:
    '''
    Checking photo in broken media group
    :param photo: str
    :return: bool
    '''
    logger = logging.getLogger(__name__)
    try:
        check_foto = requests.get(url=photo, timeout=30)
        if check_foto.status_code == 200:
            return True
    except requests.exceptions.RequestException as exc:
        logger.error(exc, exc_info=exc)