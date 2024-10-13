import jwt  # pip install pyjwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone


# 处理 JWT 令牌
# 创建用于 JWT 令牌签名的随机密钥。
# 使用以下命令，生成安全的随机密钥：
# `openssl rand -hex 32`
# 然后，把生成的密钥复制到变量**SECRET_KEY**，注意，不要使用本例所示的密钥。
SECRET_KEY = "1adfd4ad5236f9c900216606775b5668f3265c08ce35c8c31c2dd8c4ddffbc91"
# 创建指定 JWT 令牌签名算法的变量 ALGORITHM，本例中的值为 "HS256"。
ALGORITHM = "HS256"
# 创建设置令牌过期时间的变量。
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 创建生成新的 JWT 访问令牌
# 创建过期时间
now = datetime.now(timezone.utc)
print(f"now: {now}")
# now: 2024-09-08 09:40:46.529348+00:00
expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
print(f"expire: {expire}")
# expire: 2024-09-08 10:10:46.529348+00:00

# 编码的数据, sub 中存储需要的数据
to_encode = {"sub": "johndoe", "login_time": now.timestamp(), "exp": expire}

access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
print(f"access_token: {access_token}")
# access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzI1NzkwMjQ2fQ.VIih-sSeVhpu0kGco2Bt2en4TrTi4rKMBvRT7cr4HAs


try:
    # 解码 JWT 令牌
    payload: dict = jwt.decode(access_token, SECRET_KEY, [ALGORITHM])
    print(f"payload: {payload}")
    # payload: {'sub': 'johndoe', 'login_time': 1728817601.134391, 'exp': 1728819401}

    sub: str = payload.get("sub")
    print(f"sub: {sub}")
    # sub: johndoe

    login_time: datetime = datetime.fromtimestamp(payload.get("login_time"), tz=timezone.utc)
    print(f"login_time: {login_time}")
    # login_time: 2024-10-13 11:06:41.134391+00:00

    exp_time: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
    print(f"exp_time: {exp_time}")
    # exp_time: 2024-10-13 11:36:41+00:00

# JWT 令牌过期后会抛出 jwt.exceptions.ExpiredSignatureError 异常
except ExpiredSignatureError:
    print("token expired")

# 无效的 JWT 令牌会抛出 jwt.exceptions.InvalidTokenError 异常
except InvalidTokenError:
    print("Invalid token")


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
