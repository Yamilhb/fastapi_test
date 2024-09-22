from bd.database import Base

from sqlalchemy import Column, Integer, String, Float


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    Title = Column(String)
    Year = Column(Float)
    