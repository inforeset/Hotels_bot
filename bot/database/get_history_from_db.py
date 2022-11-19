from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from bot.database.models import History


def get_history_db(user_id: int, session: Session) -> List[History]:
    """
    Get history records from db
    :param user_id: int
    :param session: Session
    :return: List[History]
    """
    history_request = session.execute(
        select(History).where(History.telegram_id == user_id)
    )
    return history_request.scalars().all()