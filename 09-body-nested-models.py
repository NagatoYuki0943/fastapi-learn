# https://fastapi.tiangolo.com/zh/tutorial/body-nested-models/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class Image(BaseModel):
    url: HttpUrl    # 该字符串将被检查是否为有效的 URL
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()              # 标签不应该重复,因此使用set,会自动去重
    image: list[Image] | None = None    # 嵌套模型


class Offer(BaseModel):
    name: str
    items: list[Item]   # 深度嵌套模型


# 嵌套模型
# http://127.0.0.1:8001/docs
@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# 深度嵌套模型
# http://127.0.0.1:8001/docs
@app.put("/offers")
async def update_item(offer: Offer):
    return offer


# 纯列表请求体
@app.post("/images")
async def images(images: list[Image]):
    return images


# 任意 dict 构成的请求体
@app.post("/weights")
async def weights(weights: dict[int, float]):
    return weights


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
