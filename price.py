from json import JSONDecodeError

import requests
import json

from requests import Response

import config
import dbworker

from loguru import logger


def get_request(url: str, headers: str, params: {}) -> Response:
    """Функция для выполнения запроса"""
    try:
        return requests.get(url=url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as exc:
        logger.exception(exc)


def request_city(city: str) -> str:
    """Функция для запроса к API и получения данных о городе"""
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    try:
        request = get_request(url=url, headers=config.headers, params=querystring)
        data = json.loads(request.text)
        coordinates = f'{data["suggestions"][0]["entities"][0]["latitude"]}+{data["suggestions"][0]["entities"][0]["longitude"]}'
        return f'{data["suggestions"][0]["entities"][0]["destinationId"]}|{data["suggestions"][0]["entities"][0]["name"]}|{coordinates}'
    except LookupError as exc:
        logger.exception(exc)


def parse_list(parse_list: list, uid: str, city: str, distance: str) -> list:
    """Функция для подготовки данных к записи в бд"""
    hotels = []
    hotel_id, name, adress, center, price = '', '', '', 'нет данных', ''

    for hotel in parse_list:
        try:
            hotel_id = hotel['id']
            name = hotel['name']
            adress = f'{hotel["address"]["countryName"]}, {city.capitalize()}, {hotel["address"].get("postalCode", "")}, {hotel["address"].get("streetAddress", "")}'
            if len(hotel['landmarks']) > 0:
                if hotel['landmarks'][0]['label'] == 'Центр города':
                    center = hotel['landmarks'][0]['distance']
            price = str(hotel['ratePlan']['price']['exactCurrent'])
            coordinates = f"{hotel['coordinate'].get('lat', 0)},{hotel['coordinate'].get('lon', 0)}"
            star_rating = str(hotel['starRating'])
            user_rating = hotel.get('guestReviews', {}).get('rating', 'нет данных').replace(',', '.')
            if distance != '':
                if float(distance) < float(center.split()[0].replace(',', '.')):
                    return hotels
            hotels.append((uid, hotel_id, name, adress, center, price, coordinates, star_rating, user_rating))
        except (LookupError, ValueError) as exc:
            logger.exception(exc)
            continue
    return hotels


def request_list(id: str, list_param: list) -> list:
    """Функция для запроса к API и получения основных данных"""
    url = "https://hotels4.p.rapidapi.com/properties/list"
    checkIn = '-'.join(list_param[1].split('.')[::-1])
    checkOut = '-'.join(list_param[2].split('.')[::-1])
    sortOrder = ''
    landmarkIds = ''
    priceMin = ''
    priceMax = ''
    pageSize = list_param[4]
    if list_param[6] == '/lowprice':
        sortOrder = 'PRICE'
    elif list_param[6] == '/highprice':
        sortOrder = 'PRICE_HIGHEST_FIRST'
    elif list_param[6] == '/bestdeal':
        sortOrder = 'DISTANCE_FROM_LANDMARK'
        landmarkIds = 'Центр города'
        priceMin = list_param[7]
        priceMax = list_param[8]

    querystring = {"destinationId": id, "pageNumber": "1", "pageSize": pageSize, "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": "1", "priceMin": priceMin, "priceMax": priceMax,
                   "sortOrder": sortOrder, "locale": "ru_RU", "currency": "RUB",
                   "landmarkIds": landmarkIds}
    try:
        request = get_request(url=url, headers=config.headers, params=querystring)
        data = json.loads(request.text)
        parsed = parse_list(parse_list=data['data']['body']['searchResults']['results'], uid=list_param[5],
                            city=list_param[0], distance=list_param[9])
        return parsed
    except (LookupError, JSONDecodeError, TypeError) as exc:
        logger.exception(exc)


def request_photo(id_hotel: str) -> list:
    """Функция для запроса к API и получения данных о фотографиях"""
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    photos = []
    try:
        response = get_request(url, headers=config.headers, params=querystring)
        data = json.loads(response.text)
        for photo in data['hotelImages']:
            url = photo['baseUrl'].replace('_{size}', '_z')
            photos.append((id_hotel, url))
        return photos
    except (JSONDecodeError, TypeError) as exc:
        logger.exception(exc)


def start(list_par: list) -> tuple:
    """Основная функция модуля"""
    photos = []
    hotels = request_list(id=list_par[10], list_param=list_par)
    if hotels is not None:
        for hotel in hotels:
            if list_par[3] == '0':
                break
            if not dbworker.check_photo(hotel_id=hotel[1]):
                request_p = request_photo(id_hotel=hotel[1])
                if request_p is not None:
                    photos.extend(request_p)
        return hotels, photos
    return None, None


def check_foto(photo: str) -> bool:
    """Функция для проверки URL фото"""
    try:
        check_foto = requests.get(url=photo, timeout=30)
        if check_foto.status_code == 200:
            return True
    except requests.exceptions.RequestException as exc:
        logger.exception(exc)
