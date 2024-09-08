# https://fastapi.tiangolo.com/zh/tutorial/schema-extra-example/
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # 已经废弃的 Config 类, 请使用每个字段的 Field 或 Annotated 类代替
    # https://claude.ai/chat/7732a202-0acb-4e58-a623-c1e9b563f6ae
    # class Config:
        # schema_extra = {
        #     "example": {                # docs中默认的例子
        #         "name": "Foo",
        #         "description": "A very nice Item",
        #         "price": 35.4,
        #         "tax": 3.2,
        #     }
        # }


# Field 的附加参数
# 在 Field, Path, Query, Body 和其他你之后将会看到的工厂函数，你可以为JSON 模式声明额外信息，
# 你也可以通过给工厂函数传递其他的任意参数来给JSON 模式声明额外信息，比如增加 example:
class Food(BaseModel):
    name: str = Field(example="meat")   # Field也可以用example设置默认提示
    description: str | None = Field(default=None, example="good meat")
    price: float = Field(example=5.3)
    tax: float | None = Field(default=None, example=0.5)


# http://127.0.0.1:8000/docs
@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# http://127.0.0.1:8000/docs
@app.post("/items1/{item_id}")
async def update_item1(item_id: int, food: Food):
    results = {"item_id": item_id, "food": food}
    return results


# Body 额外参数
# 你可以通过传递额外信息给 Field 同样的方式操作Path, Query, Body等。
# 比如，你可以将请求体的一个 example 传递给 Body:
@app.put("/items2/{item_id}")
async def update_item2(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


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
