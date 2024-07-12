import jwt
import bcrypt

from repository.user_login_repository import LoginRepository, get_repository
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from model.user import User
from schema.user import BaseUserQueryRequest, DbUserQueryRequest, TokenResponse, TokenData, UserLoginRequest, \
    UserCreateRequest

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginService:
    def __init__(self, repo: LoginRepository):
        self.repo = repo

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_password_hash(password):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user: User = await self.repo.get_user_by_email_or_name(username=token_data.username, email=None)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def verify_password(plain_password, hashed_password):
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    async def authenticate_user(self, req: UserLoginRequest) -> User | bool:
        user = await self.repo.get_user_by_email_or_name(email=req.email, username=req.username)
        if not user:
            return False
        if not self.verify_password(req.password, bytes(user.hashed_password, "utf-8")):
            return False
        return user

    async def create_user(self, req: UserCreateRequest):
        hashed_password = self.get_password_hash(req.password)
        print(hashed_password)
        user: User = User(username=req.username, hashed_password=hashed_password, email=req.email)
        try:
            await self.repo.add_user(user)
        except Exception as ex:
            raise ex
        return {"code": 200}


async def get_login_service(repo: LoginRepository = Depends(get_repository)) -> LoginService:
    return LoginService(repo)
