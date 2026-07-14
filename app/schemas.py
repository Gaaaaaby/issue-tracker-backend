from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from .models import IssuePriority, IssueStatus


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=6)


class IssueBase(BaseModel):
    title: constr(min_length=3)
    description: constr(min_length=10)
    priority: IssuePriority


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    status: Optional[IssueStatus]
    priority: Optional[IssuePriority]


class IssueOut(IssueBase):
    id: int
    status: IssueStatus
    created_at: datetime

    class Config:
        orm_mode = True


class IssueSummary(BaseModel):
    total: int
    abierto: int
    en_progreso: int
    completado: int
