from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schema.user import TokenResponse, UserLoginRequest, UserCreateRequest
from service.user_login_service import get_login_service, LoginService

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()


@router.post("/token")
async def login_for_access_token(
        # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        form_data=Depends(OAuth2PasswordRequestForm),
        login_service: LoginService = Depends(get_login_service)
) -> TokenResponse:
    req: UserLoginRequest = UserLoginRequest(username=form_data.username, password=form_data.password)
    user = await login_service.authenticate_user(req)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = login_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me")
async def read_users_me(
        token: str,
        login_service: LoginService = Depends(get_login_service),
):
    current_user = login_service.get_current_user(token=token)
    return await current_user


@router.post("/register")
async def user_register(req: UserCreateRequest,
                        login_service: LoginService = Depends(get_login_service)):
    return await login_service.create_user(req)
