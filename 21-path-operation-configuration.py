# https://fastapi.tiangolo.com/zh/tutorial/path-operation-configuration/
import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


# status_code 状态码
# status_code 用于定义路径操作响应中的 HTTP 状态码。
# 可以直接传递 int 代码， 比如 404。
# http://127.0.0.1:8000/docs
@app.post("/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED
)
async def create_item(item: Item):
    return item


# tags 参数
# tags 参数的值是由 str 组成的 list （一般只有一个 str ），tags 用于为路径操作添加标签
# 路径装饰器还支持 summary 和 description 这两个参数
# http://127.0.0.1:8000/docs
@app.post("/items1",
    response_model=Item,
    tags=["items"],
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item1(item: Item):
    return item


# 文档字符串（docstring）
# 描述内容比较长且占用多行时，可以在函数的 docstring 中声明路径操作的描述，FastAPI 支持从文档字符串中读取描述内容。
# http://127.0.0.1:8000/docs
@app.get("/items2",
    response_model=list[Item],
    tags=["items"],
)
async def read_items2():
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return [{"name": "Foo", "price": 42}]



# response_description 参数用于定义响应的描述说明
#   OpenAPI 规定每个路径操作都要有响应描述
#   如果没有定义响应描述，FastAPI 则自动生成内容为 "Successful response" 的响应描述。
# http://127.0.0.1:8000/docs
@app.get("/users",
    tags=["users"],
    response_description="The created users",
)
async def read_users():
    return [{"username": "johndoe"}]


# 弃用路径操作
# deprecated 参数可以把路径操作标记为弃用，无需直接删除：
@app.get("/elements/",
    tags=["items"],
    deprecated=True
)
async def read_elements():
    return [{"item_id": "Foo"}]


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
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
