# https://fastapi.tiangolo.com/zh/tutorial/extra-models/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr # pip install pydantic[email]
from enum import Enum


app = FastAPI()


# 通过继承减少代码量
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


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
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


class ItemID(str, Enum):
    item1 = "item1"
    item2 = "item2"


items = {
    ItemID.item1: {"description": "All my friends drive a low rider", "type": "car"},
    ItemID.item2: {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# 多种相应类型
@app.get("/items/{item_id}", response_model= PlaneItem | CarItem)
async def read_item(item_id: ItemID):
    return items[item_id]


# 任意 dict 构成的响应
# 你还可以使用一个任意的普通 dict 声明响应，仅声明键和值的类型，而不使用 Pydantic 模型。
@app.get("/keyword/", response_model=dict[str, float])
async def read_keyword():
    return {"foo": 2.3, "bar": 3.4}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
