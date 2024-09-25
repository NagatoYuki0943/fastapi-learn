# https://fastapi.tiangolo.com/zh/tutorial/security/get-current-user/
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 上一章中，（基于依赖注入系统的）安全系统向*路径操作函数*传递了 str 类型的 token：
# 但这并不实用。
# 接下来，我们学习如何返回当前用户。


# 创建用户模型
# 首先，让我们来创建一个用户 Pydantic 模型。
# 与使用 Pydantic 声明请求体的方式相同，我们可以在其他任何地方使用它：
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


# 创建 get_current_user 依赖项。
# 还记得依赖项支持子依赖项吗？
# get_current_user 使用 oauth2_scheme 作为依赖项。
# 与之前直接在路径操作中的做法相同，新的 get_current_user 依赖项从子依赖项 oauth2_scheme 中接收 str 类型的 token：


# 获取用户
# get_current_user 将使用我们创建的（伪）工具函数，该函数接收 str 类型的令牌并返回我们的 Pydantic User 模型
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


# 注入当前用户
# 在*路径操作* 的 Depends 中使用 get_current_user：
# 注意，此处把 current_user 的类型声明为 Pydantic 的 User 模型。
# 这有助于在函数内部使用代码补全和类型检查。
# http://127.0.0.1:8000/docs
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


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
