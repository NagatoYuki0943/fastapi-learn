# https://fastapi.tiangolo.com/zh/tutorial/body-nested-models/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class Image(BaseModel):
    # 除了普通的单一值类型（如 str、int、float 等）外，你还可以使用从 str 继承的更复杂的单一值类型。
    url: HttpUrl  # 该字符串将被检查是否为有效的 URL
    name: str


# 嵌套模型
# Pydantic 模型的每个属性都具有类型。
# 但是这个类型本身可以是另一个 Pydantic 模型。
# 因此，你可以声明拥有特定属性名称、类型和校验的深度嵌套的 JSON 对象。
# 上述这些都可以任意的嵌套。
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()  # 标签不应该重复,因此使用set,会自动去重
    image: list[Image] | None = None  # 将子模型用作类型


class Offer(BaseModel):
    name: str
    items: list[Item]  # 深度嵌套模型


# 嵌套模型
# http://127.0.0.1:8000/docs
@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# 深度嵌套模型
# http://127.0.0.1:8000/docs
@app.put("/offers")
async def create_offer(offer: Offer):
    return offer


# 纯列表请求体
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


# 任意 dict 构成的请求体
@app.post("/weights")
async def create_index_weights(weights: dict[int, float]):
    return weights


# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
