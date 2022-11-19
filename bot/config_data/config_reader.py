from dataclasses import dataclass
from os import getenv

from dotenv import find_dotenv, load_dotenv


@dataclass
class TgBot:
    token: str


@dataclass
class DB:
    host: str
    port: int
    name: str
    login: str
    password: str


@dataclass
class Redis:
    use_redis: bool
    host: str


@dataclass
class RapidApi:
    rapid_api_key: str
    max_hotel: int
    max_photo: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DB
    redis: Redis
    rapid_api: RapidApi


def load_config() -> Config:
    '''
    Load config form .env and return it
    :return: Config
    '''
    if not find_dotenv():
        exit(".env doesn't exist")
    else:
        load_dotenv()

    return Config(
        tg_bot=TgBot(
            token=getenv("BOT_TOKEN"),
        ),
        db=DB(
            host=getenv("DB_HOST"),
            port=int(getenv("DB_PORT")),
            name=getenv("DB_NAME"),
            login=getenv("DB_USER"),
            password=getenv("DB_PASS")
        ),
        redis=Redis(
            host=getenv("REDIS_HOST"),
            use_redis=getenv("USE_REDIS", 'False').lower() in ('true', '1', 't')
        ),
        rapid_api=RapidApi(
            rapid_api_key=getenv("RAPIDAPI_KEY"),
            max_hotel=int(getenv("MAX_HOTEL")),
            max_photo=int(getenv("MAX_PHOTO"))
        ),
    )
