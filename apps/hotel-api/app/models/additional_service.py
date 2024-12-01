from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class serviceModel(Base):
    __tablename__ = "additional_service"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    max_number = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)
