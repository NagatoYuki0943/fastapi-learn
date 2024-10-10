from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError


# 处理 JWT 令牌
# 创建用于 JWT 令牌签名的随机密钥。
# 使用以下命令，生成安全的随机密钥：
# `openssl rand -hex 32`
# 然后，把生成的密钥复制到变量**SECRET_KEY**，注意，不要使用本例所示的密钥。
SECRET_KEY = "1adfd4ad5236f9c900216606775b5668f3265c08ce35c8c31c2dd8c4ddffbc91"
# 创建指定 JWT 令牌签名算法的变量 ALGORITHM，本例中的值为 "HS256"。
ALGORITHM = "HS256"
# 创建设置令牌过期时间的变量。
ACCESS_TOKEN_EXPIRE_MINUTES = 15


# 定义令牌端点响应的 Pydantic 模型。
class Token(BaseModel):
    access_token: str
    token_type: str


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


# 创建生成新的访问令牌的工具函数。
def create_access_token(data: dict, expires_times: int | None = None) -> str:
    # 防止修改原数据
    to_encode = data.copy()
    # 添加过期时间
    if expires_times:
        expires_delta = timedelta(minutes=expires_times)
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 默认过期时间为 15 分钟
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> str:
    try:
        # 传入的 token 是 JWT 令牌，需要解码
        # 过期后会抛出 jwt.exceptions.ExpiredSignatureError 异常
        payload: dict = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        print(f"payload: {payload}")
        sub: str = payload.get("sub", None)
        if sub is None:
            raise credentials_exception
        return sub

    # JWT 令牌过期后会抛出 jwt.exceptions.ExpiredSignatureError 异常
    except ExpiredSignatureError:
        print("token expired")
        raise expired_exception

    # 无效的 JWT 令牌会抛出 jwt.exceptions.InvalidTokenError 异常
    except InvalidTokenError:
        print("invalid token")
        raise credentials_exception
