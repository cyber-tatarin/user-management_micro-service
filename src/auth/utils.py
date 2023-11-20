from passlib.context import CryptContext
import uuid
import jwt
from datetime import datetime, timedelta

from src.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


async def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if 'user_id' in to_encode and isinstance(to_encode['user_id'], uuid.UUID):
        to_encode['user_id'] = str(to_encode['user_id'])
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    