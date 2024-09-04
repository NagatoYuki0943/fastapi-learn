# https://fastapi.tiangolo.com/zh/tutorial/body/
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# 与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。默认值为 None 的模型属性也是可选的。
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 将请求体作为 JSON 读取
# 在函数内部，你可以直接访问模型对象的所有属性
# http://127.0.0.1:8000/docs
@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        # 在*路径操作*函数内部直接访问模型对象的属性：
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 请求体 + 路径参数
# FastAPI 支持同时声明路径参数和请求体。
# FastAPI 能识别与**路径参数**匹配的函数参数，还能识别从**请求体**中获取的类型为 Pydantic 模型的函数参数。
# http://127.0.0.1:8000/docs
@app.put("/items1/{item_id}")
async def create_item1(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


# 请求体 + 路径参数 + 查询参数
# FastAPI 支持同时声明**请求体**、路径参数**和**查询参数。
# FastAPI 能够正确识别这三种参数，并从正确的位置获取数据。
# 函数参数按如下规则进行识别：
#     - **路径**中声明了相同参数的参数，是路径参数
#     - 类型是（int、float、str、bool 等）**单类型**的参数，是**查询**参数
#     - 类型是 Pydantic 模型**的参数，是**请求体
# http://127.0.0.1:8000/items/3?q=what
@app.put("/items2/{item_id}")
async def create_item2(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


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
