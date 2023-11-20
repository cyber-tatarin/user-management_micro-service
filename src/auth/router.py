from fastapi import APIRouter, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import timedelta

from src.auth import schemas, service, dependencies, utils
from src.repositories.postgres_repository import UserRepository
from src.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(response: Response,
                user_cred: OAuth2PasswordRequestForm = Depends(),
                user_repo: UserRepository = Depends(dependencies.get_user_repository)):
    user = await service.validate_credentials(user_repo, user_cred)
    access_token = await utils.create_token(data={"user_id": user.id, "user_role": user.role},
                                            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = await utils.create_token(data={"user_id": user.id},
                                             expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.RespUser)
async def create_user(new_user_cred: schemas.NewUserCred,
                      user_repo: UserRepository = Depends(dependencies.get_user_repository)):
    new_user = await service.create_user_with_hashed_password(new_user_cred, user_repo)
    return new_user
