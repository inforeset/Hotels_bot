from bot.database.models import Hotels


def get_hotel_message(hotel: Hotels, period: int) -> str:
    """
    Form string for hotels messages
    :param hotel: Hotels
    :param period: int
    :return: str
    """
    price_period = round(hotel.price * period, 2)
    if hotel.price:
        price_period = f'{price_period} RUB'
        price = f"{hotel.price:.2f} RUB"
    else:
        price_period = 'Уточняйте в отеле'
        price = 'Уточняйте в отеле'
    string = f"🏨 Название отеля: {hotel.name}\n" \
             f"🌎 Адрес: {hotel.adress}\n" \
             f"🌐 Сайт: https://www.hotels.com/ho{hotel.hotel_id}\n" \
             f"📌 Открыть в Google maps: http://maps.google.com/maps?z=12&t=m&q=loc:{hotel.coordinates}" \
             f"\n↔ Расстояние от центра: {hotel.center:.2f} км" \
             f"\n💳 Цена за период: {price_period}" \
             f"\n1️⃣ Цена за сутки: {price}" \
             f"\n⭐ Рейтинг: {hotel.star_rates:.2f}" \
             f"\n✨ Рейтинг по мнению посетителей: {hotel.user_rates if hotel.user_rates else 'нет данных'}"
    return string
