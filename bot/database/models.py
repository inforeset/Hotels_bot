from sqlalchemy import Column, Integer, BigInteger, Boolean, Date, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID

from bot.database.base import Base


class History(Base):
    __tablename__ = "history"

    telegram_id = Column(BigInteger, nullable=False, index=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    command = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    distance = Column(Integer, nullable=True)
    error = Column(Boolean, nullable=False)
    period = Column(Integer, nullable=False)
    price_max = Column(Integer, nullable=True)
    price_min = Column(Integer, nullable=True)
    quantity_display = Column(Integer, nullable=False)
    quantity_photo = Column(Integer, nullable=False)


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('history.id', ondelete='CASCADE'), nullable=False, index=True)
    hotel_id = Column(BigInteger, nullable=False, index=True)  #
    center = Column(Numeric, nullable=False)
    coordinates = Column(String, nullable=False)
    adress = Column(String, nullable=True)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    star_rates = Column(Numeric, nullable=True)
    user_rates = Column(Numeric, nullable=True)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(BigInteger, nullable=False, index=True)
    photo = Column(String, nullable=False)
