# https://fastapi.tiangolo.com/zh/tutorial/body-fields/
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
# 注意，Field 是直接从 pydantic 导入的，而不是像其他的（Query，Path，Body 等）都从 fastapi 导入。
# Field 的工作方式和 Query、Path 和 Body 相同，包括它们的参数等等也完全相同。


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0,   # 必须大于0
        description="The price must be greater than zero"
    )
    tax: float | None = None


# http://127.0.0.1:8001/docs
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body()):
    results = {"item_id": item_id, "item": item}
    return results


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
