import logging
import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from telebot import TeleBot, StateMemoryStorage
from telebot.custom_filters import StateFilter, TextMatchFilter, IsDigitFilter
from telebot.storage import StateRedisStorage

from bot.config_data.config_reader import load_config
from bot.filters.city_filter import CitiesCallbackFilter
from bot.filters.price_max import PriceMaxFilter
from bot.filters.range_filter import MessageInRangeFilter
from bot.filters.private import IsPrivateChatFilter
from bot.handlers.callback.calendar import register_calendar_callback
from bot.handlers.callback.choice_city import register_city_callback
from bot.handlers.callback.with_photo import register_load_photo_callback
from bot.handlers.callback.without_photo import register_no_photo_callback
from bot.handlers.commands.hello import register_start
from bot.handlers.commands.help import register_help
from bot.handlers.commands.hi_low_best import register_commands_price
from bot.handlers.commands.history import register_get_history
from bot.handlers.commands.reset_handler import register_reset_all
from bot.handlers.messages.check_out import register_check_out
from bot.handlers.messages.check_out_wrong import register_check_out_wrong
from bot.handlers.messages.distance import register_get_distance
from bot.handlers.messages.distance_wrong import register_get_distance_wrong
from bot.handlers.messages.get_city import register_city
from bot.handlers.default_handlers.echo import register_echo
from bot.handlers.messages.price_max import register_get_price_max
from bot.handlers.messages.price_max_wrong import register_get_price_max_wrong
from bot.handlers.messages.price_min import register_get_price_min
from bot.handlers.messages.price_min_wrong import register_get_price_min_wrong
from bot.handlers.messages.quantity_hotels import register_quantity
from bot.handlers.messages.quantity_hotels_wrong import register_quantity_wrong
from bot.handlers.messages.quantity_photo import register_get_quantity_photo
from bot.handlers.messages.quantity_photo_wrong import register_get_quantity_photo_wrong
from bot.middlewares.config import ConfigMiddleware
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.logging import LoggingMiddleware

from bot.database.utils import make_connection_string


def register_all_middlewares(bot):
    bot.setup_middleware(LoggingMiddleware())
    bot.setup_middleware(DbSessionMiddleware(db_pool))
    bot.setup_middleware(ConfigMiddleware(config=config))


def register_all_filters(bot):
    bot.add_custom_filter(IsPrivateChatFilter())
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(MessageInRangeFilter())
    bot.add_custom_filter(CitiesCallbackFilter())
    bot.add_custom_filter(TextMatchFilter())
    bot.add_custom_filter(IsDigitFilter())
    bot.add_custom_filter(PriceMaxFilter(bot))


def register_all_handlers(bot):
    register_reset_all(bot)
    register_commands_price(bot)
    register_city(bot)
    register_quantity(bot)
    register_city_callback(bot)
    register_quantity_wrong(bot)
    register_check_out(bot)
    register_check_out_wrong(bot)
    register_get_distance(bot)
    register_get_distance_wrong(bot)
    register_get_price_max(bot)
    register_get_price_max_wrong(bot)
    register_get_price_min(bot)
    register_get_price_min_wrong(bot)
    register_get_quantity_photo(bot)
    register_get_quantity_photo_wrong(bot)
    register_calendar_callback(bot)
    register_load_photo_callback(bot)
    register_no_photo_callback(bot)
    register_start(bot)
    register_help(bot)
    register_get_history(bot)
    register_echo(bot)


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("start bot")

    # Reading config file
    config = load_config()

    # Creating DB engine for PostgreSQL
    engine = create_engine(
        make_connection_string(config.db),
        future=True,
        echo=False
    )

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=Session)

    storage = StateMemoryStorage() if not config.redis.use_redis else StateRedisStorage(host=config.redis.host)

    bot = TeleBot(token=config.tg_bot.token, state_storage=storage, use_class_middlewares=True)

    register_all_middlewares(bot)
    register_all_filters(bot)
    register_all_handlers(bot)

    try:
        logger.info('start polling')
        bot.polling(skip_pending=True, none_stop=True)
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped, have a nice day')
    finally:
        engine.dispose()
