from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.sql_engine import Base


class roleModel(Base):
    __tablename__ = "role_permission"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)


class roleUserModel(Base):
    __tablename__ = "role_user"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role_permission.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(Date)
    updated_at = Column(Date)
