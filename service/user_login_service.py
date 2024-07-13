import jwt
import bcrypt

from loguru import logger
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from model.user import User
from repository.user_login_repository import LoginRepository, get_repository
from schema.user import BaseUserQueryRequest, DbUserQueryRequest, TokenResponse, TokenData, UserLoginRequest, \
    UserCreateRequest, BaseUserQueryResponse

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginService:
    def __init__(self, repo: LoginRepository):
        self.repo = repo

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Response | BaseUserQueryResponse:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return Response(status_code=status.HTTP_401_UNAUTHORIZED)
            token_data = TokenData(username=username)
        except InvalidTokenError as error:
            logger.error(error)
            return Response(content="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
        user: User = await self.repo.get_user_by_email_or_name(username=token_data.username, email=None)
        if user is None:
            return Response(content="User not found", status_code=status.HTTP_404_NOT_FOUND)
        return BaseUserQueryResponse(**user.to_dict())

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    async def authenticate_user(self, req: UserLoginRequest) -> User | bool:
        user = await self.repo.get_user_by_email_or_name(email=req.email, username=req.username)
        if not user:
            return False
        if not self.verify_password(req.password, bytes(user.hashed_password, "utf-8")):
            return False
        return user

    async def create_user(self, req: UserCreateRequest) -> Response | BaseUserQueryResponse:
        hashed_password = self.get_password_hash(req.password)
        user: User = User(username=req.username, hashed_password=hashed_password, email=req.email)
        try:
            user = await self.repo.add_user(user)
        except Exception as ex:
            logger.error(ex)
            return Response("Internal Server Error!", status_code=500)
        return BaseUserQueryResponse(**user.to_dict())


async def get_login_service(repo: LoginRepository = Depends(get_repository)) -> LoginService:
    return LoginService(repo)
