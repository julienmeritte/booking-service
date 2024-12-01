from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class room_category(Base):
    __tablename__ = "room_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    max_occupancy = Column(Integer)
    rate = Column(DECIMAL)
