from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class reservationServiceModel(Base):
    __tablename__ = "reservation_additional_service"
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), nullable=False)
    additional_service_id = Column(
        Integer, ForeignKey("additional_service.id"), nullable=False
    )
    created_at = Column(Date)
    updated_at = Column(Date)
