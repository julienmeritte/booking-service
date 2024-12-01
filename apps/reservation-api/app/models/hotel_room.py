from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class roomModel(Base):
    __tablename__ = "hotel_room"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    room_number = Column(String)
    category_id = Column(Integer, ForeignKey("room_category.id"), nullable=False)
    created_at = Column(Date)
    updated_at = Column(Date)
