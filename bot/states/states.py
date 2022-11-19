# States group.
from telebot.handler_backends import StatesGroup, State


class HotelsStates(StatesGroup):
    start = State()
    enter_city = State()
    quantity = State()
    check_in = State()
    check_out = State()
    photo = State()
    quantity_photo = State()
    price_min = State()
    price_max = State()
    distance = State()
    final = State()
