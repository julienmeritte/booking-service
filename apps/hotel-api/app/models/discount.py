from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class discountModel(Base):
    __tablename__ = "discount"
    id = Column(Integer, primary_key=True, index=True)
    discount_type_id = Column(Integer, ForeignKey("discount_type.id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(Date)
    updated_at = Column(Date)
