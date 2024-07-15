from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from model.user import User
from schema.user import TokenResponse, UserLoginRequest, UserCreateRequest, BaseUserQueryResponse
from service.user_login_service import get_login_service, LoginService
from const import LoginError

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(
        # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        form_data=Depends(OAuth2PasswordRequestForm),
        login_service: LoginService = Depends(get_login_service)):
    req: UserLoginRequest = UserLoginRequest(username=form_data.username, password=form_data.password)
    user = await login_service.authenticate_user(req)
    if isinstance(user, User):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = login_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return TokenResponse(access_token=access_token, token_type="bearer")
    elif user == LoginError.USER_NOT_FOUND:
        return JSONResponse(content={"msg": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    elif user == LoginError.INCORRECT_PASSWORD:
        return JSONResponse(content={"msg": "Incorrect user or password!"}, status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/me", response_model=BaseUserQueryResponse, status_code=status.HTTP_200_OK)
async def read_users_me(
        token: str,
        login_service: LoginService = Depends(get_login_service),
):
    return await login_service.get_current_user(token=token)


@router.post("/register", response_model=BaseUserQueryResponse, status_code=status.HTTP_201_CREATED)
async def user_register(req: UserCreateRequest,
                        login_service: LoginService = Depends(get_login_service)):
    return await login_service.create_user(req)
