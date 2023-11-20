import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class NewUserCred(BaseModel):
    email: EmailStr
    password: str


class RespUser(BaseModel):
    id: uuid.UUID
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    