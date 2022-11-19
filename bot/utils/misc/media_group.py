from typing import List

from telebot.types import InputMediaPhoto

from bot.utils.request.check_photo_in_group import check_foto


def form_media_group(photos: List, error: bool = False) -> List[InputMediaPhoto]:
    """
    Form media group, and check photo if send group failed
    :param photos: List
    :param error: bool
    :return: List[InputMediaPhoto]
    """
    media = []
    for photo in photos:
        if error and check_foto(photo=photo.photo):
            continue
        media.append(InputMediaPhoto(media=photo.photo))
    return media
