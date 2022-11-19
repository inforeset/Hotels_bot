from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_photo_kb() -> InlineKeyboardMarkup:
    """
    Return inline keyboard for photo question
    :return:  InlineKeyboardMarkup
    """
    city_kb_markup = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Да', callback_data='yes')
    key_no = InlineKeyboardButton(text='Нет', callback_data='no')
    city_kb_markup.add(key_yes, key_no)
    return city_kb_markup
