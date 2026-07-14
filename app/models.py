from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum


class IssuePriority(str, enum.Enum):
    alta = "alta"
    media = "media"
    baja = "baja"


class IssueStatus(str, enum.Enum):
    abierto = "abierto"
    en_progreso = "en progreso"
    completado = "completado"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(IssuePriority), nullable=False, default=IssuePriority.media)
    status = Column(Enum(IssueStatus), nullable=False, default=IssueStatus.abierto)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
