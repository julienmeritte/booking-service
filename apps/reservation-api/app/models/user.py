from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from app.sql_engine import Base

class userModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String)
    password = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)
