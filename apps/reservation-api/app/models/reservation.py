from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class reservationModel(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("hotel_room.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    number_occupants = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(Date)
    updated_at = Column(Date)
