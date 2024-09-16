# https://fastapi.tiangolo.com/zh/tutorial/body-fields/
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
# 注意，Field 是直接从 pydantic 导入的，而不是像其他的（Query，Path，Body 等）都从 fastapi 导入。
# Field 的工作方式和 Query、Path 和 Body 相同，包括它们的参数等等也完全相同。


app = FastAPI()


# Field 的工作方式和 Query、Path、Body 相同，参数也相同。
# 实际上，Query、Path 都是 Params 的子类，而 Params 类又是 Pydantic 中 FieldInfo 的子类。
# Pydantic 的 Field 返回也是 FieldInfo 的类实例。
# Body 直接返回的也是 FieldInfo 的子类的对象。后文还会介绍一些 Body 的子类。
# 注意，从 fastapi 导入的 Query、Path 等对象实际上都是返回特殊类的函数。
class Item(BaseModel):
    name: str
    # 使用 Field 定义模型的属性
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0,  # 必须大于0
        description="The price must be greater than zero",
    )
    tax: float | None = None


# Body(embed=True) 嵌入单个请求体参数
# http://127.0.0.1:8000/docs
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
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
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
