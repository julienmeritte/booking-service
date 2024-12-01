from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class discountTypeModel(Base):
    __tablename__ = "discount_type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)
