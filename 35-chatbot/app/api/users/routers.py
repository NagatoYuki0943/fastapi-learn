import datetime
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ...core import Session
from ...models import UserDB

from ...dependencies import (
    create_access_token,
    verify_access_token,
    get_password_hash,
    verify_password,
    oauth2_scheme,
)


router = APIRouter()
# 可以使用它来声明*路径操作*。
# 使用方式与 FastAPI 类相同：
# 你可以将 APIRouter 视为一个「迷你 FastAPI」类。
# 所有相同的选项都得到支持。
# 所有相同的 parameters、responses、dependencies、tags 等等。


# 创建数据库会话
session = Session()


# 定义令牌端点响应的 Pydantic 模型。
class Token(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=256, example="johndoe")
    email: EmailStr
    phone: str | None = Field(None, example="")

    class Config:
        from_attributes = True


class UserOutSchema(UserSchema):
    password: str = Field(..., min_length=6, max_length=256, example="123456")


class UserInDBSchema(UserSchema):
    id: int
    hashed_password: str
    last_login_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None = None


# 从数据库中获取用户。
def get_user(email: str) -> UserInDBSchema | None:
    user = session.query(UserDB).filter(UserDB.email == email).first()
    if user:
        # 更新登录时间
        user.last_login_at = datetime.datetime.now()
        session.commit()
        # return UserInDBSchema.from_orm(user)
        return UserInDBSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=user.password,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
        )


def get_activate_user(email: str) -> UserInDBSchema | None:
    user = get_user(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    elif user.deleted_at is None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )


# 验证用户名和密码，并返回用户。
def authenticate_user(
    username: str,
    password: str,
) -> UserInDBSchema | None:
    user = get_activate_user(username)

    # 密码是否正确
    if verify_password(password, user.hashed_password):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=UserSchema)
async def register(
    new_user: UserOutSchema,
) -> UserSchema:
    print(f"{new_user = }")
    existing_user = get_user(new_user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # 加密密码
    hashed_password = get_password_hash(new_user.password)
    # 创建新用户
    user = UserDB(
        username=new_user.username,
        password=hashed_password,
        email=new_user.email,
        phone=new_user.phone,
    )
    session.add(user)
    session.commit()
    return new_user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # 验证用户名和密码
    user = authenticate_user(form_data.username, form_data.password)

    # 创建生成新的 JWT 访问令牌
    access_token = create_access_token(data={"sub": user.id})
    # 返回 JWT 访问令牌的 Pydantic 模型
    return Token(access_token=access_token, token_type="bearer")


async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str | None:
    sub = verify_access_token(token)
    print(f"{sub = }")
    if sub is not None:
        return sub


@router.get("/test_auth")
async def test_auth(
    sub: Annotated[UserInDBSchema, Depends(get_access_token)],
) -> dict:
    return {"sub": sub}
