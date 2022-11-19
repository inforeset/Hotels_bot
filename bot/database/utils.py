from bot.config_data.config_reader import DB


def make_connection_string(db: DB) -> str:
    """
    Make connection string to db
    :param db: DB
    :return: str
    """
    result = f"postgresql+psycopg2://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    return result
