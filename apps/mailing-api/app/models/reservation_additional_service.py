from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class reservation_additional_service(Base):
    __tablename__ = "reservation_additional_service"
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), nullable=False)
    additional_service_id = Column(Integer, ForeignKey("additional_service.id"), nullable=False)
