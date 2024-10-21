# https://fastapi.tiangolo.com/zh/tutorial/response-model/
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr  # pip install pydantic[email]


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


# 响应模型
# 你可以在任意的路径操作中使用 response_model 参数来声明用于响应的模型：
#   - @app.get()
#   - @app.post()
#   - @app.put()
#   - @app.delete()
#   - 等等
# 注意，response_model是「装饰器」方法（get，post 等）的一个参数。不像之前的所有参数和请求体，它不属于路径操作函数。
# http://127.0.0.1:8000/docs
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return item


# 它接收的类型与你将为 Pydantic 模型属性所声明的类型相同，因此它可以是一个 Pydantic 模型，但也可以是一个由 Pydantic 模型组成的 list，例如 List[Item]
# FastAPI 将使用此 response_model 来：
#     - 将输出数据转换为其声明的类型。
#     - 校验数据。
#     - 在 OpenAPI 的*路径操作*中为响应添加一个 JSON Schema。
#     - 并在自动生成文档系统中使用。
# 但最重要的是：
#     - 会将输出数据限制在该模型定义内。下面我们会看到这一点有多重要。
# http://127.0.0.1:8000/docs
@app.get("/items1", response_model=list[Item])
async def read_items1():
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.1, "tax": 1.5},
    ]


# 我们可以创建一个有明文密码的输入模型和一个没有明文密码的输出模型：
# 这样，即便我们的路径操作函数将会返回包含密码的相同输入用户
# ..我们已经将 response_model 声明为了不包含密码的 UserOut 模型：
# 将 response_model 声明为了不包含密码的 UserOut 模型
# 因此，FastAPI 将会负责过滤掉未在输出模型中声明的所有数据（使用 Pydantic）
@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn):
    return user


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# 响应模型可以具有默认值
# description: str | None = None 具有默认值 None。
# tax: float = 10.5 具有默认值 10.5.
# tags: list[str] = [] 具有一个空列表作为默认值： [].
# 但如果它们并没有存储实际的值，你可能想从结果中忽略它们的默认值
# 你可以设置*路径操作装饰器*的 response_model_exclude_unset=True 参数：
@app.post("/items2/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item2(item_id: str):
    return items[item_id]


# 你还可以使用路径操作装饰器的 response_model_include 和 response_model_exclude 参数
# 它们接收一个由属性名称 str 组成的 set 来包含（忽略其他的）或者排除（包含其他的）这些属性
# 如果你只有一个 Pydantic 模型，并且想要从输出中移除一些数据，则可以使用这种快捷方法。
#     但是依然建议你使用上面提到的主意，使用多个类而不是这些参数。
#     这是因为即使使用 response_model_include 或 response_model_exclude 来省略某些属性，在应用程序的 OpenAPI 定义（和文档）中生成的 JSON Schema 仍将是完整的模型。
#     这也适用于作用类似的 response_model_by_alias。
# 如果你忘记使用 set 而是使用 list 或 tuple，FastAPI 仍会将其转换为 set 并且正常工作
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# 使用 list 而不是 set
# 如果你忘记使用 set 而是使用 list 或 tuple，FastAPI 仍会将其转换为 set 并且正常工作：
@app.get(
    "/items/{item_id}/name1",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name1(item_id: str):
    return items[item_id]


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
