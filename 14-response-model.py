# https://fastapi.tiangolo.com/zh/tutorial/response-model/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr # pip install pydantic[email]
from enum import Enum


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = 0.1
    tags: list[str] = []


# 有密码
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# 返回时不要密码
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# 你可以在任意的路径操作中使用 response_model 参数来声明用于响应的模型：
#   @app.get()
#   @app.post()
#   @app.put()
#   @app.delete()
# 注意，response_model是「装饰器」方法（get，post 等）的一个参数。不像之前的所有参数和请求体，它不属于路径操作函数。
# http://127.0.0.1:8001/docs
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return item


# 它接收的类型与你将为 Pydantic 模型属性所声明的类型相同，因此它可以是一个 Pydantic 模型，但也可以是一个由 Pydantic 模型组成的 list，例如 List[Item]
# http://127.0.0.1:8001/docs
@app.get("/items1", response_model=list[Item])
async def read_items1():
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.1, "tax": 1.5},
    ]


# 即便我们的路径操作函数将会返回包含密码的相同输入用户
# 将 response_model 声明为了不包含密码的 UserOut 模型
# 因此，FastAPI 将会负责过滤掉未在输出模型中声明的所有数据（使用 Pydantic）
@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn):
    return user


class ItemID(str, Enum):
    foo = "foo"
    bar = "bar"
    baz = "baz"


items = {
    ItemID.foo: {"name": "Foo", "price": 50.2},
    ItemID.bar: {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    ItemID.baz: {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}, # 这里的值和默认值
}
# 响应模型可以具有默认值
# 但如果它们并没有存储实际的值，你可能想从结果中忽略它们的默认值
# 使用 response_model_exclude_unset 参数,可以忽略没有实际存储的值
@app.post(
    "/items2/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True
)
async def create_item2(item_id: ItemID):
    return items[item_id]


# 你还可以使用路径操作装饰器的 response_model_include 和 response_model_exclude 参数
# 它们接收一个由属性名称 str 组成的 set 来包含（忽略其他的）或者排除（包含其他的）这些属性
# 如果你忘记使用 set 而是使用 list 或 tuple，FastAPI 仍会将其转换为 set 并且正常工作
@app.get(
    "/items3",
    response_model=Item,
    response_model_include={"name", "description"}  # 包含 等同于 {"name", "description"} set(["name", "description"])
)
async def create_item3():
    return {"name": "Baz", "description": "What", "price": 50.2, "tax": 10.5, "tags": []}


@app.get(
    "/items4",
    response_model=Item,
    response_model_exclude={"tax", "tags"}          # 忽略
)
async def create_item4():
    return {"name": "Baz", "description": "What", "price": 50.2, "tax": 10.5, "tags": []}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
