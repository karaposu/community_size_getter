# models.py
from sqlalchemy import Column, Integer, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CommunitySize(Base):
    __tablename__ = 'community_size'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    value_date = Column(DateTime, nullable=False)
    fill_date = Column(DateTime, nullable=False)

    twitter = Column(Integer, nullable=False)
    reddit = Column(Integer, nullable=False)
    discord = Column(Integer, nullable=False)
    telegram = Column(Integer, nullable=False)

    price_in_usdt = Column(Numeric(20, 8), nullable=False)
    marcetcap = Column(Numeric(20, 8), nullable=False)
