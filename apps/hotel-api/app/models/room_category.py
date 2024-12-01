from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class roomCategoryModel(Base):
    __tablename__ = "room_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    max_occupancy = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)
