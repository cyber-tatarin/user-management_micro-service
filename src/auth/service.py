import uuid
import jwt
import os
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

from src.config import get_config
from src.auth import utils, models

load_dotenv('.env')

settings = get_config(os.getenv("CONFIG"))

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def create_access_token(data: dict):
    to_encode = data.copy()
    if 'user_id' in to_encode and isinstance(to_encode['user_id'], uuid.UUID):
        to_encode['user_id'] = str(to_encode['user_id'])
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id = str(payload.get("user_id"))
#         if id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id=id)
#     except jwt.PyJWTError:
#         raise credentials_exception
#     return token_data


# async def get_current_user(token: str = Depends(oath2_scheme),
#                      user_repo: UserRepository = Depends(utils.get_user_repository)):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='Could not validate credentials',
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#
#     token_data = verify_access_token(token, credential_exception)
#     user = user_repo.get_by_id(token_data.id)
#     return user


async def validate_credentials(user_repo, user_cred):
    user = await user_repo.get_by_email(user_cred.username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    return user


async def create_user_with_hashed_password(new_user_cred, user_repo):
    hashed_pwd = utils.pwd_context.hash(new_user_cred.password)
    new_user_cred.password = hashed_pwd
    new_user = models.User(**new_user_cred.model_dump())
    try:
        await user_repo.add(new_user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Error code: {e.code}")
    return new_user
