# https://fastapi.tiangolo.com/zh/tutorial/schema-extra-example/
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {                # docs中默认的例子
                "name": "NNNNName",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class Food(BaseModel):
    name: str = Field(example="meat")   # Field也可以用example设置默认提示
    description: str | None = Field(default=None, example="good meat")
    price: float = Field(example=5.3)
    tax: float | None = Field(default=None, example=0.5)


# http://127.0.0.1:8000/docs
@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item, food: Food):
    results = {"item_id": item_id, "item": item, "food": food}
    return results


@app.put("/items1/{item_id}")
async def update_item1(
    item_id: int,
    item: Item = Body(  # 使用body设置默认参数
        example={
            "name": "NNNNName",
            "description": "A very nice Item",
            "price": 15.3,
            "tax": 3.0,
        },
    )
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
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
