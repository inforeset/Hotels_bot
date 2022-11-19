from bot.database.models import History


def get_history_message(record: History) -> str:
    """
    Form string for history message
    :param record: History
    :return: str
    """
    string = f'Дата и время запроса: {record.date_time:%d.%m.%Y %H:%M}' \
             f'\nКоманда: {record.command}' \
             f'\nГород: {record.city}' \
             f'\nКоличество отелей для поиска: {record.quantity_display}' \
             f'\nДата заезда: {record.check_in:%d.%m.%Y}' \
             f'\nДата выезда: {record.check_out:%d.%m.%Y}'
    if record.command == '/bestdeal':
        string += f'\nМинимальная цена за ночь: {record.price_min} RUB' \
                  f'\nМаксимальное цена за ночь: {record.price_max} RUB' \
                  f'\nМаксимальное расстояние от центра: {record.distance} км'
    return string
