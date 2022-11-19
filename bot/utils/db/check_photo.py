from sqlalchemy.orm import Session, Query

from bot.database.models import Photo


def photo_exist(hotel_id: str, session: Session) -> Query:
    """
    Check existing photo in db
    :param hotel_id: str
    :param session: Session
    :return: Query
    """
    q = session.query(Photo).filter(Photo.hotel_id == hotel_id)
    return session.query(q.exists()).scalar()
