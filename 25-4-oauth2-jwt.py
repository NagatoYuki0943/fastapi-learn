# https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# passlib 和 bcrypt 用于密码哈希, 验证密码成功后返回 JWT 令牌
# from passlib.context import CryptContext    # pip install passlib bcrypt==4.0.1
import bcrypt  # pip install bcrypt

# PyJWT 用于生成和验证 JWT 令牌(每次前端都传递令牌，服务器验证令牌后才允许访问)
import jwt  # pip install pyjwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError


# OAuth2 实现密码哈希与 Bearer JWT 令牌验证
# 至此，我们已经编写了所有安全流，本章学习如何使用 JWT 令牌（Token）和安全密码哈希（Hash）实现真正的安全机制。
# 本章的示例代码真正实现了在应用的数据库中保存哈希密码等功能。
# 接下来，我们紧接上一章，继续完善安全机制。

# JWT 简介
# JWT 即**JSON 网络令牌**（JSON Web Tokens）。
# JWT 是一种将 JSON 对象编码为没有空格，且难以理解的长字符串的标准。JWT 的内容如下所示：
#     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
# JWT 字符串没有加密，任何人都能用它恢复原始信息。
# 但 JWT 使用了签名机制。接受令牌时，可以用签名校验令牌。
# 使用 JWT 创建有效期为一周的令牌。第二天，用户持令牌再次访问时，仍为登录状态。
# 令牌于一周后过期，届时，用户身份验证就会失败。只有再次登录，才能获得新的令牌。如果用户（或第三方）篡改令牌的过期时间，因为签名不匹配会导致身份验证失败。
# 如需深入了解 JWT 令牌，了解它的工作方式，请参阅 https://jwt.io。
# `pip install pyjwt`

# 密码哈希
# **哈希**是指把特定内容（本例中为密码）转换为乱码形式的字节序列（其实就是字符串）。
# 每次传入完全相同的内容时（比如，完全相同的密码），返回的都是完全相同的乱码。
# 但这个乱码无法转换回传入的密码。
# 为什么使用密码哈希
# 原因很简单，假如数据库被盗，窃贼无法获取用户的明文密码，得到的只是哈希值。
# 这样一来，窃贼就无法在其它应用中使用窃取的密码（要知道，很多用户在所有系统中都使用相同的密码，风险超大）。

# passlib 甚至可以读取 Django、Flask 的安全插件等工具创建的密码。
# 例如，把 Django 应用的数据共享给 FastAPI 应用的数据库。或利用同一个数据库，可以逐步把应用从 Django 迁移到 FastAPI。
# 并且，用户可以同时从 Django 应用或 FastAPI 应用登录。
# `pip install passlib[bcrypt]`


# 用户名: johndoe 密码: secret
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$VQoTe7XFivUfmUCLSpv.recCY2UrseBxdWVW1dMz1RfxVPyL1SbJW",
        "disabled": False,
    }
}


# 处理 JWT 令牌
# 创建用于 JWT 令牌签名的随机密钥。
# 使用以下命令，生成安全的随机密钥：
# `openssl rand -hex 32`
# 然后，把生成的密钥复制到变量**SECRET_KEY**，注意，不要使用本例所示的密钥。
SECRET_KEY = "1adfd4ad5236f9c900216606775b5668f3265c08ce35c8c31c2dd8c4ddffbc91"
# 创建指定 JWT 令牌签名算法的变量 ALGORITHM，本例中的值为 "HS256"。
ALGORITHM = "HS256"
# 创建设置令牌过期时间的变量。
ACCESS_TOKEN_EXPIRE_MINUTES = 1


# 定义令牌端点响应的 Pydantic 模型。
class Token(BaseModel):
    access_token: str
    token_type: str


# 创建生成新的访问令牌的工具函数。
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # 防止修改原数据
    to_encode = data.copy()
    # 添加过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 默认过期时间为 15 分钟
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


app = FastAPI()


# passlib 对于同一个字符串每次生成的哈希值都不同。
# PassLib 对于同一个字符串每次生成不同的哈希值主要是通过使用"盐"(salt)来实现的。
# 盐是一个随机生成的字符串，每次哈希时都会生成一个新的盐。
#   - 当你使用 PassLib 对密码进行哈希时，它会自动生成一个随机盐。
#   - 将这个盐与原始密码组合。
#   - 对组合后的字符串进行哈希运算。
#   - 最终的哈希值通常包含盐和哈希结果。
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 接下来，创建三个工具函数，其中一个函数用于哈希用户的密码。
# 第一个函数用于校验接收的密码是否匹配存储的哈希值。
# 第三个函数用于身份验证，并返回用户。
def verify_password(plain_password, hashed_password) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return bcrypt.checkpw(plain_password.encode("utf8"), hashed_password.encode("utf8"))


def get_password_hash(password) -> str:
    # return pwd_context.hash(password)
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")


# 从数据库中获取用户。
def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 验证用户名和密码，并返回用户。
def authenticate_user(
    fake_db, username: str, password: str
) -> UserInDB | Literal[False]:
    user = get_user(fake_db, username)
    # 用户是否存在
    if not user:
        return False
    # 验证密码是否正确
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 创建 OAuth2 密码端点。
# 该端点用于获取 JWT 访问令牌。
# 该端点需要用户名和密码，并返回 JWT 访问令牌。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT 验证异常
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
# JWT 过期异常
expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired",
    headers={"WWW-Authenticate": "Bearer"},
)


# 获取当前用户, 并验证 JWT 令牌。
# JWT sub 的技术细节
# JWT 规范还包括 sub 键，值是令牌的主题。
# 该键是可选的，但要把用户标识放在这个键里，所以本例使用了该键。
# 除了识别用户与许可用户在 API 上直接执行操作之外，JWT 还可能用于其它事情。
# 例如，识别**汽车**或**博客**。
# 接着，为实体添加权限，比如**驾驶**（汽车）或**编辑**（博客）。
# 然后，把 JWT 令牌交给用户（或机器人），他们就可以执行驾驶汽车，或编辑博客等操作。无需注册账户，只要有 API 生成的 JWT 令牌就可以。
# 同理，JWT 可以用于更复杂的场景。
# 在这些情况下，多个实体的 ID 可能是相同的，以 ID foo 为例，用户的 ID 是 foo，车的 ID 是 foo，博客的 ID 也是 foo。
# 为了避免 ID 冲突，在给用户创建 JWT 令牌时，可以为 sub 键的值加上前缀，例如 username:。因此，在本例中，sub 的值可以是：username:johndoe。
# 注意，划重点，sub 键在整个应用中应该只有一个唯一的标识符，而且应该是字符串。
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        # 传入的 token 是 JWT 令牌，需要解码
        # 过期后会抛出 jwt.exceptions.ExpiredSignatureError 异常
        payload: dict = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        print(f"payload: {payload}")
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    # JWT 令牌过期后会抛出 jwt.exceptions.ExpiredSignatureError 异常
    except ExpiredSignatureError:
        print("token expired")
        raise expired_exception

    # 无效的 JWT 令牌会抛出 jwt.exceptions.InvalidTokenError 异常
    except InvalidTokenError:
        print("invalid token")
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# 获取当前用户，并验证其是否已激活。
async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# 更新 /token 路径操作, 可以将 /token 改为 /login, 不过 OAuth2PasswordBearer 中也要更改为 login
# 用令牌过期时间创建 timedelta 对象。
# 创建并返回真正的 JWT 访问令牌。
# http://127.0.0.1:8000/docs
@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # 验证用户名和密码
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建生成新的 JWT 访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # 返回 JWT 访问令牌的 Pydantic 模型
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
) -> User:
    return current_user


# 在使用 johndoe 和 secret 登录之后,请求 users/me 路径时的请求如下
# curl -X 'GET' \
#   'http://127.0.0.1:8000/users/me/' \
#   -H 'accept: application/json' \
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzI1Nzg3OTQyfQ.Gnd91OQeiZXWQ9U5ls-Fz9mvGXjeShuLerRBpMRzOaA'
# 这就是 JWT Token 身份验证的过程。


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path
    import uvicorn

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
