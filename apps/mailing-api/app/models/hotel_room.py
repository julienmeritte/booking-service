from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class hotel_room(Base):
    __tablename__ = "hotel_room"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    room_number = Column(String)
    category_id = Column(Integer, ForeignKey("room_category.id"), nullable=False)
