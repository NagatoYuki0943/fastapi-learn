# https://fastapi.tiangolo.com/zh/tutorial/security/get-current-user/
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



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


# get_current_user 将使用我们创建的（伪）工具函数，该函数接收 str 类型的令牌并返回我们的 Pydantic User 模型
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


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

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv('PORT', 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv('HOST', '0.0.0.0')

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
