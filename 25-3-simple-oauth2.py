# https://fastapi.tiangolo.com/zh/tutorial/security/simple-oauth2/
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


# OAuth2 实现简单的 Password 和 Bearer 验证
# 本章添加上一章示例中欠缺的部分，实现完整的安全流。

# 获取 username 和 password
# 首先，使用 FastAPI 安全工具获取 username 和 password。
# OAuth2 规范要求使用**密码流**时，客户端或用户必须以表单数据形式发送 username 和 password 字段。
# 并且，这两个字段必须命名为 username 和 password ，不能使用 user-name 或 email 等其它名称。
# 不过也不用担心，前端仍可以显示终端用户所需的名称。
# 数据库模型也可以使用所需的名称。
# 但对于登录*路径操作*，则要使用兼容规范的 username 和 password，（例如，实现与 API 文档集成）。
# 该规范要求必须以表单数据形式发送 username 和 password，因此，不能使用 JSON 对象。

# Scope（作用域）
# OAuth2 还支持客户端发送**scope**表单字段。
# 虽然表单字段的名称是 scope（单数），但实际上，它是以空格分隔的，由多个**scope**组成的长字符串。
# **作用域**只是不带空格的字符串。
# 常用于声明指定安全权限，例如：
# 常见用例为，users:read 或 users:write
# 脸书和 Instagram 使用 instagram_basic
# 谷歌使用 https://www.googleapis.com/auth/drive
# "说明"
#   OAuth2 中，**作用域**只是声明指定权限的字符串。
#   是否使用冒号 : 等符号，或是不是 URL 并不重要。
#   这些细节只是特定的实现方式。
#   对 OAuth2 来说，都只是字符串而已。


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# 更新依赖项
# 接下来，更新依赖项。
# 使之仅在当前用户为激活状态时，才能获取 current_user。
# 为此，要再创建一个依赖项 get_current_active_user，此依赖项以 get_current_user 依赖项为基础。
# 如果用户不存在，或状态为未激活，这两个依赖项都会返回 HTTP 错误。
# 因此，在端点中，只有当用户存在、通过身份验证、且状态为激活时，才能获得该用户：

# 创建 OAuth2 密码端点。
# 该端点用于获取 Bearer 访问令牌。
# 该端点需要用户名和密码，并返回 Bearer 访问令牌。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# "说明"
# 此处返回值为 Bearer 的响应头 WWW-Authenticate 也是规范的一部分。
# 任何 401**UNAUTHORIZED**HTTP（错误）状态码都应返回 WWW-Authenticate 响应头。
# 本例中，因为使用的是 Bearer Token，该响应头的值应为 Bearer。
# 实际上，忽略这个附加响应头，也不会有什么问题。
# 之所以在此提供这个附加响应头，是为了符合规范的要求。
# 说不定什么时候，就有工具用得上它，而且，开发者或用户也可能用得上。
# 这就是遵循标准的好处……
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# 获取 username 和 password 的代码
# 接下来，使用 FastAPI 工具获取用户名与密码。
# OAuth2PasswordRequestForm
# 首先，导入 OAuth2PasswordRequestForm，然后，在 /token 路径操作 中，用 Depends 把该类作为依赖项。
# OAuth2PasswordRequestForm 是用以下几项内容声明表单请求体的类依赖项：
# - username
# - password
# - 可选的 scope 字段，由多个空格分隔的字符串组成的长字符串
# - 可选的 grant_type

# ** post("/token") 和 OAuth2PasswordBearer(tokenUrl="token") 中的 url 必须相同 **
# https://claude.ai/chat/b67ba070-c27f-42e9-8173-4a3487ebc399
#   1. 这两个 URL 是相匹配的，这不是巧合，而是有意为之。OAuth2PasswordBearer 中的 tokenUrl 应该与实际处理登录请求的端点 URL 相匹配。
#   2. 这种匹配是必要的，因为 OAuth2PasswordBearer 使用 tokenUrl 来告诉 OpenAPI（Swagger）文档在哪里可以获取令牌。
#      当用户尝试在 Swagger UI 中进行身份验证时，它会知道向哪个 URL 发送凭证。
#   3. 然而，URL 本身不必一定是 "token"。您可以选择任何有意义的 URL 路径，
#      只要保证 OAuth2PasswordBearer 中的 tokenUrl 和实际的登录端点 URL 保持一致即可。例如，可以将它们都改为 "/login"：


# form_data: OAuth2PasswordRequestForm = Depends() 依赖注入快捷方式
# http://127.0.0.1:8000/docs
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 用户名是否存在
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    # 密码是否正确
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 返回 Token
    # token 端点的响应必须是 JSON 对象。
    # 响应返回的内容应该包含 token_type。本例中用的是**Bearer**Token，因此， Token 类型应为**bearer**。
    # 返回内容还应包含 access_token 字段，它是包含权限 Token 的字符串。
    # 本例只是简单的演示，返回的 Token 就是 username，但这种方式极不安全。
    return {"access_token": user.username, "token_type": "bearer"}
    # "提示"
    # 按规范的要求，应像本示例一样，返回带有 access_token 和 token_type 的 JSON 对象。
    # 这是开发者必须在代码中自行完成的工作，并且要确保使用这些 JSON 的键。
    # 这几乎是唯一需要开发者牢记在心，并按规范要求正确执行的事。
    # FastAPI 则负责处理其它的工作。


# http://127.0.0.1:8000/docs
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    print(current_user)
    return current_user


# 在使用 johndoe 和 secret 登录之后,请求 users/me 路径时的请求如下
#   curl -X 'GET' \
#       'http://127.0.0.1:8000/users/me' \
#       -H 'accept: application/json' \
#       -H 'Authorization: Bearer johndoe'  # 使用 johndoe 的 Bearer token 进行身份验证
# 这就是 Bearer Token 身份验证的过程。


# run: uvicorn main:app --reload --host=0.0.0.0 --port=8000
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
