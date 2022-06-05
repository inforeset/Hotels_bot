import datetime
import uuid
from typing import Union

import telebot
from telebot import types

import config
import dbworker
import price as p

from loguru import logger
from telegram_bot_calendar import WYearTelegramCalendar, LSTEP

if __name__ == '__main__':
    bot = telebot.TeleBot(token=config.token)
    globalVar = {}
    dbworker.create_tables()
    logger.add('logs/logs_{time}.log', level='DEBUG', format="{time} {level} {message}", rotation="06:00",
               compression="zip")
    logger.debug('Error')
    logger.info('Information message')
    logger.warning('Warning')
    LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}

class MyStyleCalendar(WYearTelegramCalendar):
    # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = ""
    empty_year_button = ""


def form_media_group(photos: list, error: bool = False) -> list:
    """Функция для формирования медиагруппы, если возникла ошибка, то производим проверку ссылок в группе"""
    media = []
    for photo in photos:
        if error and p.check_foto(photo=photo[0]):
            continue
        media.append(types.InputMediaPhoto(media=photo[0]))
    return media


def reset(id: Union[str, int]) -> None:
    """Функция для сброса состояния"""
    dbworker.set_state(id=str(id), state=config.States.S_START.value)
    help(id=id)


def work(id: Union[str, int]) -> None:
    """Основная функция, обрабатывает ответы пользователя и формирует запросы к API и БД"""
    error = False
    city = globalVar[id]['city']
    datet = globalVar[id]['datetime']
    check_in = globalVar[id]['check_in']
    check_out = globalVar[id]['check_out']
    quantity_photos = globalVar[id]['quantity_photos']
    quantity = globalVar[id]['quantity']
    command = globalVar[id]['command']
    uid = globalVar[id]['uid']
    price_min = globalVar[id].get('price_min', '')
    price_max = globalVar[id].get('price_max', '')
    distance = globalVar[id].get('distance', '')
    period = globalVar[id]['period']
    destination_id = globalVar[id]['destination_id']
    try:
        load = bot.send_animation(chat_id=id,
                                  animation='CgACAgIAAxkDAAIF9GJIBSTAGTfAnNTwq5sE_K6x3guAAAKfFwAC71JASk1brYyEpiWZIwQ',
                                  caption='Загружаю...')
    except:
        load = bot.send_message(chat_id=id, text='Ищем...')
    hotels, photos = p.start(
        list_par=[city, check_in, check_out, quantity_photos, quantity, uid, command, price_min, price_max,
                  distance, destination_id])
    if hotels is None:
        error = True
    history = (
        uid, str(id), datet, city, check_in, check_out, quantity, quantity_photos, error, command, price_min,
        price_max, distance, period)
    if dbworker.set_history(history=history) and not error:
        if dbworker.set_hotels(hotels=hotels) and quantity_photos != '0' and len(photos) > 0:
            dbworker.set_photos(photos=photos)
    bot.delete_message(chat_id=id, message_id=load.message_id)
    if error:
        bot.send_message(chat_id=id, text="Что-то пошло не так")
        reset(id=id)
    else:
        if len(hotels) == 0:
            bot.send_message(chat_id=id, text="По вашему запросу ничего не найдено")
        else:
            for hotel in hotels:
                bot.send_message(chat_id=id, text=
                f"🏨 Название отеля: {hotel[2]}"
                f"\n🌎 Адрес: {hotel[3]}"
                f"\n🌐 Сайт: https://www.hotels.com/ho{hotel[1]}"
                f"\n📌 Открыть в Google maps: http://maps.google.com/maps?z=12&t=m&q=loc:{hotel[6]}"
                f"\n↔ Расстояние от центра: {hotel[4]}"
                f"\n💳 Цена за период: {round(float(hotel[5]) * int(period))} RUB"
                f"\n1️⃣ Цена за сутки: {round(float(hotel[5]))} RUB"
                f"\n🔜 Дата заезда: {check_in}"
                f"\n🔙 Дата выезда: {check_out}"
                f"\n⭐ Рейтинг: {hotel[7]}"
                f"\n✨ Рейтинг по мнению посетителей: {hotel[8]}", disable_web_page_preview=True)
                if quantity_photos != '0':
                    photos_h = dbworker.get_photos(hotel_id=hotel[1], limit=quantity_photos)
                    if photos_h:
                        media = form_media_group(photos=photos_h)
                        if len(media) != 0:
                            try:
                                bot.send_media_group(chat_id=id, media=media)
                            except:
                                media = form_media_group(photos=photos_h, error=True)
                                if len(media) != 0:
                                    bot.send_media_group(chat_id=id, media=media)
                                else:
                                    bot.send_message(chat_id=id, text='Фотографии не найдены')
                    else:
                        bot.send_message(chat_id=id, text='Фотографии не найдены')
            help(id=id)


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def price(message: types.Message) -> None:
    bot.send_message(chat_id=message.chat.id, text="В каком городе будем искать?")
    globalVar[message.chat.id] = {}
    globalVar[message.chat.id]['command'] = message.text
    globalVar[message.chat.id]['datetime'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    globalVar[message.chat.id]['uid'] = str(uuid.uuid1())
    dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_CITY.value)


@bot.message_handler(commands=["history"])
def history(message: types.Message) -> None:
    history = dbworker.get_history(id=str(message.chat.id))
    if history:
        for record in history:
            period = record[10]
            error = record[11]
            uid = record[12]
            string = f'Дата и время запроса: {record[1]}' \
                     f'\nКоманда: {record[2]}' \
                     f'\nГород: {record[3]}' \
                     f'\nКоличество отелей для поиска: {record[4]}' \
                     f'\nДата заезда: {record[5]}' \
                     f'\nДата выезда: {record[6]}'
            if record[2] == '/bestdeal':
                string += f'\nМинимальная цена за ночь: {record[7]} RUB' \
                          f'\nМаксимальное цена за ночь: {record[8]} RUB' \
                          f'\nМаксимальное расстояние от центра: {record[9]} км'
            bot.send_message(chat_id=message.chat.id, text=string)
            if error:
                bot.send_message(chat_id=message.chat.id, text='\nПри загрузке возникли ошибки, отели не загружены')
            else:
                hotels = dbworker.get_hotels(uid=uid)
                if hotels:
                    for hotel in hotels:
                        bot.send_message(chat_id=message.chat.id, text=
                        f"🏨 Название отеля: {hotel[0]}"
                        f"\n🌎 Адрес: {hotel[1]}"
                        f"\n🌐 Сайт: https://www.hotels.com/ho{hotel[2]}"
                        f"\n📌 Открыть в Google maps: http://maps.google.com/maps?z=12&t=m&q=loc:{hotel[3]}"
                        f"\n↔ Расстояние от центра: {hotel[6]}"
                        f"\n💳 Цена за период: {round(float(hotel[7]) * int(period))} RUB"
                        f"\n1️⃣ Цена за сутки: {round(float(hotel[7]))} RUB"
                        f"\n⭐ Рейтинг: {hotel[4]}"
                        f"\n✨ Рейтинг по мнению посетителей: {hotel[5]}",
                                         disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=message.chat.id, text='Записей не найдено')
    help(id=message.chat.id)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_CITY.value)
def get_city(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
        return
    load = bot.send_message(chat_id=message.chat.id, text="Веду поиск...")
    city = p.request_city(city=message.text)
    bot.delete_message(chat_id=message.chat.id, message_id=load.message_id)
    if city:
        bot.send_message(chat_id=message.chat.id, text=f"Название города: {city.split('|')[1]}"
                                                       f"\n📌 Google maps: https://www.google.com/maps/@?api=1&map_action=map&center={city.split('|')[2]}&zoom=9")
        globalVar[message.chat.id]['city'] = city.split('|')[1]
        globalVar[message.chat.id]['destination_id'] = city.split('|')[0]
        keybord(id=message.chat.id, city='True')
    else:
        bot.send_message(chat_id=message.chat.id, text="Ничего не нашлось!")
        reset(id=message.chat.id)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_QUANTITY.value)
def get_quantity(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id,
                         text=f"Введите цифрами, какое количество отелей будем показывать (максимум {config.quantity_max_hotel})?")
        return
    elif 1 > int(message.text) > config.quantity_max_hotel:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Ошибка, повторите ввод. Какое количество отелей будем показывать (максимум {config.quantity_max_hotel})?")
        return
    else:
        globalVar[message.chat.id]['quantity'] = message.text
        bot.send_message(chat_id=message.chat.id, text="Планируемая дата заезда (дд.мм.гггг)?")
        dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_CHECKIN.value)
        my_calendar(id=message.chat.id)


def my_calendar(id):
    calendar, step = MyStyleCalendar(locale='ru', min_date=datetime.date.today()).build()
    bot.send_message(id, f"Выберите {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=MyStyleCalendar.func())
def cal(c):
    result, key, step = MyStyleCalendar(locale='ru', min_date=datetime.date.today()).process(c.data)
    if c.data == "cbcal_0_n":
        bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
        reset(id=c.message.chat.id)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id)
        globalVar[c.message.chat.id]['check_in'] = result.strftime('%m.%d.%Y')
        bot.send_message(chat_id=c.message.chat.id, text="Планируемое кол-во дней?")
        dbworker.set_state(id=str(c.message.chat.id), state=config.States.S_ENTER_CHECKOUT.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_CHECKOUT.value)
def get_check_out(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id, text="Ошибка, введите цифрами. Кол-во дней")
        return
    elif 1 > int(message.text):
        bot.send_message(chat_id=message.chat.id, text="Ошибка, повторите ввод. Кол-во дней?")
        return
    else:
        globalVar[message.chat.id][
            'check_out'] = f"{(datetime.datetime.strptime(globalVar[message.chat.id]['check_in'], '%d.%m.%Y') + datetime.timedelta(days=int(message.text))).strftime('%d.%m.%Y')}"
        globalVar[message.chat.id]['period'] = message.text
        if globalVar[message.chat.id]['command'] == '/bestdeal':
            bot.send_message(chat_id=message.chat.id, text="Введите минимальную цену (руб/сут)")
            dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_PRICEMIN.value)
        else:
            dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_PHOTO.value)
            keybord(id=message.chat.id)


def keybord(id: Union[str, int], city: Union[str, None] = None):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    if city is None:
        callback_data_yes = 'yes'
        callback_data_no = 'no'
        question = 'Будем загружать и выводить фото для каждого отеля?'
    else:
        callback_data_yes = 'city'
        callback_data_no = 'no_city'
        question = 'Это правильное расположение?'
    key_yes = types.InlineKeyboardButton(text='Да', callback_data=callback_data_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data=callback_data_no)
    keyboard.add(key_yes, key_no)
    bot.send_message(chat_id=id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: types.CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    if call.data == "yes":
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'Количество фотографий для каждого отеля (максимум {config.quantity_max_photo})?')
        dbworker.set_state(id=str(call.message.chat.id), state=config.States.S_ENTER_QUANTITYPHOTO.value)
    elif call.data == "no":
        globalVar[call.message.chat.id]['quantity_photos'] = '0'
        dbworker.set_state(id=str(call.message.chat.id), state=config.States.S_START.value)
        work(id=call.message.chat.id)
    elif call.data == "no_city":
        reset(id=call.message.chat.id)
    elif call.data == "city":
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Какое количество отелей будем показывать (максимум {config.quantity_max_hotel})?")
        dbworker.set_state(id=str(call.message.chat.id), state=config.States.S_ENTER_QUANTITY.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(
        id=message.chat.id) == config.States.S_ENTER_QUANTITYPHOTO.value)
def get_quantity_photos(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id,
                         text=f"Введите цифрами, количество фотографий для каждого отеля (максимум {config.quantity_max_photo})?")
        return
    elif 1 > int(message.text) > config.quantity_max_photo:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Ошибка. Количество фотографий для каждого отеля (максимум {config.quantity_max_photo})?")
        return
    else:
        globalVar[message.chat.id]['quantity_photos'] = message.text
        dbworker.set_state(id=str(message.chat.id), state=config.States.S_START.value)
        work(id=message.chat.id)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_PRICEMIN.value)
def get_pricemin(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id, text="Введите цифрами минимальную цену (руб/сут)")
        return
    elif 1 > int(message.text):
        bot.send_message(chat_id=message.chat.id, text="Некорректный ввод, введите минимальную цену (руб/сут)")
        return
    else:
        if message.text == '0':
            price_min = '1'
        else:
            price_min = message.text
        globalVar[message.chat.id]['price_min'] = price_min
        bot.send_message(chat_id=message.chat.id, text="Введите максимальную цену (руб/сут)")
        dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_PRICEMAX.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_PRICEMAX.value)
def get_pricemax(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id, text="Введите цифрами максимальную цену (руб/сут)")
        return
    elif 1 > int(message.text) < int(globalVar[message.chat.id]['price_min']):
        bot.send_message(chat_id=message.chat.id, text="Ошибка ввода, введите максимальную цену (руб/сут)")
        return
    else:
        globalVar[message.chat.id]['price_max'] = message.text
        bot.send_message(chat_id=message.chat.id, text="Введите максимальное расстояние от центра (км)")
        dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_DISTANCE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(id=message.chat.id) == config.States.S_ENTER_DISTANCE.value)
def get_distance(message: types.Message) -> None:
    if message.text == '/reset':
        reset(id=message.chat.id)
    elif not message.text.isdigit():
        bot.send_message(chat_id=message.chat.id, text="Введите цифрами максимальное расстояние от центра (км)")
        return
    elif 1 > float(message.text):
        bot.send_message(chat_id=message.chat.id, text="Ошибка, введите максимальное расстояние от центра (км)")
        return
    else:
        globalVar[message.chat.id]['distance'] = message.text
        dbworker.set_state(id=str(message.chat.id), state=config.States.S_ENTER_QUANTITYPHOTO.value)
        keybord(id=message.chat.id)


def help(id: Union[int, str]) -> None:
    bot.send_message(chat_id=id, text="/lowprice — вывод самых дешёвых отелей в городе\n"
                                      "/highprice — вывод самых дорогих отелей в городе\n"
                                      "/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n"
                                      "/history — вывод истории поиска отелей\n"
                                      "/reset - выход в меню")


@bot.message_handler(content_types=['text'])
def start(message: types.Message) -> None:
    if message.text.lower() == "привет" or message.text.lower() == "/hello-world" or message.text.lower() == "/start":
        bot.send_message(chat_id=message.chat.id, text="Привет, для получения списка команд набери /help")
    elif message.text == "/help" or message.text == "/reset":
        help(id=message.chat.id)
    else:
        bot.send_message(chat_id=message.chat.id, text="Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
