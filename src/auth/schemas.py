import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class NewUserCred(BaseModel):
    email: EmailStr
    password: str

    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True
        

class RespUser(BaseModel):
    id: uuid.UUID
    created_at: datetime

    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    