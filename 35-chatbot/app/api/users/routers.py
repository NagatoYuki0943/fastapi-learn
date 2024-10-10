from typing import Annotated, Literal

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


session = Session()


# 定义令牌端点响应的 Pydantic 模型。
class Token(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr
    phone: str | None = Field(None, example="")

    class Config:
        from_attributes = True


class UserOutSchema(UserSchema):
    password: str = Field(..., min_length=8, max_length=100, example="password123")


class UserInDBSchema(UserSchema):
    hashed_password: str


router = APIRouter()
# 可以使用它来声明*路径操作*。
# 使用方式与 FastAPI 类相同：
# 你可以将 APIRouter 视为一个「迷你 FastAPI」类。
# 所有相同的选项都得到支持。
# 所有相同的 parameters、responses、dependencies、tags 等等。


# 从数据库中获取用户。
def get_user(email: str) -> UserInDBSchema | None:
    user = session.query(UserDB).filter(UserDB.email==email).first()
    if user:
        return UserInDBSchema(
            username = user.username,
            email = user.email,
            phone = user.phone,
            hashed_password = user.password,
        )


# 验证用户名和密码，并返回用户。
def authenticate_user(
    username: str,
    password: str,
) -> UserInDBSchema | Literal[False]:
    user = get_user(username)
    # 用户是否存在
    if not user:
        return False
    # 验证密码是否正确
    if not verify_password(password, user.hashed_password):
        return False
    return user


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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建生成新的 JWT 访问令牌
    access_token = create_access_token(data={"sub": user.username})
    # 返回 JWT 访问令牌的 Pydantic 模型
    return Token(access_token=access_token, token_type="bearer")


async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDBSchema:
    sub = verify_access_token(token)
    if sub is not None:
        return sub


@router.get("/test_auth")
async def test_auth(
    sub: Annotated[UserInDBSchema, Depends(get_access_token)],
) -> dict:
    return {"sub": sub}
