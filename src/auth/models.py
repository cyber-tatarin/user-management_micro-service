from sqlalchemy import Column, String, Enum, Boolean, DateTime, func, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

import uuid
import enum


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=func.now())

    users = relationship("User", back_populates="groups", lazy='subquery')


class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(70))
    surname = Column(String(70))
    username = Column(String(70), unique=True)
    phone_number = Column(String(16), unique=True)
    email = Column(String(90), unique=True)
    password = Column(String(64))
    role = Column(Enum(Role))
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    image_s3_path = Column(Text)
    is_blocked = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())

    groups = relationship("Group", back_populates="users", lazy='joined')
