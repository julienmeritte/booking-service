from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DECIMAL
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class additional_service(Base):
    __tablename__ = "additional_service"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rate = Column(DECIMAL)
