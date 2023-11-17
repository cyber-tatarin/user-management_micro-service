from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.auth import schemas, utils, service, dependencies
from src.repositories.postgres_repository import UserRepository

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(),
                user_repo: UserRepository = Depends(dependencies.get_user_repository)):
    
    user = await service.validate_credentials(user_repo, user_cred)
    access_token = await service.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.RespUser)
async def create_user(new_user_cred: schemas.NewUserCred,
                      user_repo: UserRepository = Depends(dependencies.get_user_repository)):
    new_user = await service.create_user_with_hashed_password(new_user_cred, user_repo)
    return new_user
