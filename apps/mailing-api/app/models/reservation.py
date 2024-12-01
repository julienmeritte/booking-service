from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("hotel_room.id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    total_rate = Column(DECIMAL)
