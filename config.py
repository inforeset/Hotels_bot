from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('BOT_TOKEN') #Name: Hotels t.me/BestSearchingHotelsBot

db_file = "base.db"
headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY')
}
quantity_max_hotel = 10
quantity_max_photo = 5


class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_CITY = "1"
    S_ENTER_QUANTITY = "2"
    S_ENTER_CHECKIN = "3"
    S_ENTER_CHECKOUT = "4"
    S_ENTER_PHOTO = "5"
    S_ENTER_QUANTITYPHOTO = "6"
    S_ENTER_PRICEMIN = "7"
    S_ENTER_PRICEMAX = "8"
    S_ENTER_DISTANCE = "9"
