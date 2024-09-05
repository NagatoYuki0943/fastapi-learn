# https://fastapi.tiangolo.com/zh/tutorial/extra-models/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr # pip install pydantic[email]
from enum import Enum


app = FastAPI()


# 更多模型
# 书接上文，多个关联模型这种情况很常见。
# 特别是用户模型，因为：
#     **输入模型**应该含密码
#     **输出模型**不应含密码
#     **数据库模型**需要加密的密码


# **user_in.model_dump() 简介
# Pydantic 的 .model_dump()
# user_in 是类 UserIn 的 Pydantic 模型。
# Pydantic 模型支持 .model_dump() 方法，能返回包含模型数据的**字典**。
# 因此，如果使用如下方式创建 Pydantic 对象 user_in：
#     user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
# 就能以如下方式调用：
#     user_dict = user_in.model_dump()
# 现在，变量 user_dict中的就是包含数据的**字典**（变量 user_dict 是字典，不是 Pydantic 模型对象）。
# 以如下方式调用：
#     print(user_dict)
# 输出的就是 Python 字典：
#     {
#         'username': 'john',
#         'password': 'secret',
#         'email': 'john.doe@example.com',
#         'full_name': None,
#     }


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# 通过继承 UserBase 减少代码量
class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    """假装加密密码"""
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    """假装存入数据库"""
    hashed_password = fake_password_hasher(user_in.password)
    # UserIn中的password不会保存进UserInDB中
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


# http://127.0.0.1:8000/docs
@app.post("/user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# Union 或者 anyOf
# 响应可以声明为两种类型的 Union 类型，即该响应可以是两种类型中的任意类型。
# 在 OpenAPI 中可以使用 anyOf 定义。# http://127.0.0.1:8000/docs
@app.get("/items/{item_id}", response_model= PlaneItem | CarItem)
async def read_item(item_id: str):
    return items[item_id]


class Item(BaseModel):
    name: str
    description: str


items1 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


# 模型列表
# 使用同样的方式也可以声明由对象列表构成的响应。
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items1


# 任意 dict 构成的响应
# 你还可以使用一个任意的普通 dict 声明响应，仅声明键和值的类型，而不使用 Pydantic 模型。
# http://127.0.0.1:8000/docs
@app.get("/keyword", response_model=dict[str, float])
async def read_keyword():
    return {"foo": 2.3, "bar": 3.4}


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
