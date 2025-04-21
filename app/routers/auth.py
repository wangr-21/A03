import datetime
import os
from typing import Annotated

import jwt
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    params,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select

from ..db import DBSession, User
from ..services import fleep

router = APIRouter(prefix="/auth", tags=["auth"])

AUTH_TOKEN_URL = "api/auth/token"  # noqa: S105  # wtf ruff
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
if SECRET_KEY is None:
    raise RuntimeError("请设置环境变量 JWT_SECRET_KEY")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user: User, plain_password: str) -> bool:
    return pwd_context.verify(plain_password, user.password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + (
        expires_delta or datetime.timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token", response_model=TokenResponse)
async def login(
    db: DBSession,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """用户登录，返回 JWT token"""

    user = await db.scalar(select(User).where(User.username == form.username))
    if user is None or not verify_password(user, form.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",  # noqa: S106  # wtf ruff
    )


@router.post("/register", response_model=RegisterResponse)
async def register(
    db: DBSession,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    name: Annotated[str, Form()],
    title: str | None = Form(None),
    department: str | None = Form(None),
    avatar: UploadFile | None = File(None),
):
    """用户注册"""

    if await db.scalar(select(User).where(User.username == form.username)):
        raise HTTPException(status_code=400, detail="User already exists")

    avatar_data = None
    if avatar:
        avatar_head = await avatar.read(256)
        avatar_info = fleep.get(avatar_head)
        if avatar_info is None or not any(
            mime.startswith("image/") for mime in avatar_info.mime
        ):
            raise HTTPException(status_code=400, detail="Invalid avatar")
        avatar_data = avatar_head + await avatar.read()
        if len(avatar_data) > 4 * 1024 * 1024:  # 4MB
            raise HTTPException(status_code=400, detail="Avatar too large")

    user = User(
        username=form.username,
        password=get_password_hash(form.password),
        name=name,
        title=title,
        department=department,
        avatar=avatar_data,
    )
    db.add(user)
    await db.commit()
    return RegisterResponse(username=form.username)


async def get_current_user(
    db: DBSession,
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl=AUTH_TOKEN_URL))],
) -> User:
    credentials_exception = lambda: HTTPException(  # noqa: E731
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (username := payload.get("sub")) is None:
            raise credentials_exception()
    except InvalidTokenError as e:
        raise credentials_exception() from e

    user = await db.scalar(select(User).where(User.username == username))
    if user is None:
        raise credentials_exception()

    await db.refresh(user)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
"""
当前登录用户的依赖项，返回 User 对象
"""


def RequireLogin() -> params.Depends:  # noqa: N802
    return Depends(get_current_user)
