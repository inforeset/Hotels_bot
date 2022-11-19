import logging

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from bot.config_data.config_reader import DB


def check_or_create_db(db: DB) -> None:
    """
    Check conncetion to db, and create DB if DB_CREATE in .env
    :param db: DB
    :return: None
    """
    connection = None
    cursor = None
    logger = logging.getLogger(__name__)
    try:
        if not db.autocreate_db:
            connection = psycopg2.connect(user=db.login,
                                          dbname=db.name,
                                          password=db.password,
                                          host=db.host,
                                          port=db.port)
        else:
            connection = psycopg2.connect(user=db.admin,
                                          password=db.admin_password,
                                          host=db.host,
                                          port=db.port)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute('SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = %s', (db.login,))
            user_exists = cursor.fetchone()
            if not user_exists:
                cursor.execute("""create user %s with password %s""", (db.login, db.password))
            cursor.execute('SELECT 1 FROM pg_catalog.pg_database WHERE datname=%s', (db.name,))
            db_exists = cursor.fetchone()
            if not db_exists:
                cursor.execute("""create database %s owner %s""", (db.name, db.login))
            logger.info('BD is ready')
    except (Exception, Error) as error:
        logger.error(error, exc_info=error)
    finally:
        if connection:
            cursor.close()
            connection.close()
