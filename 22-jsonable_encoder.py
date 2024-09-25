# https://fastapi.tiangolo.com/zh/tutorial/encoder
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()

# JSON 兼容编码器
# 在某些情况下，您可能需要将数据类型（如Pydantic模型）转换为与JSON兼容的数据类型（如dict、list等）。
# 比如，如果您需要将其存储在数据库中。
# 对于这种要求， **FastAPI**提供了jsonable_encoder()函数。

# 使用jsonable_encoder
# 让我们假设你有一个数据库名为fake_db，它只能接收与JSON兼容的数据。
# 例如，它不接收datetime这类的对象，因为这些对象与JSON不兼容。
# 因此，datetime对象必须将转换为包含ISO格式化的str类型对象。
# 同样，这个数据库也不会接收Pydantic模型（带有属性的对象），而只接收dict。


fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


# http://127.0.0.1:8000/docs
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(
        item
    )  # 将Pydantic模型转换为dict，并将datetime转换为str。
    fake_db[id] = json_compatible_item_data
    print(item)
    print(json_compatible_item_data)


# run: uvicorn main:app --reload --port=8000
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
