from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    print: float
    tax: float | None = None


app = FastAPI()


# base
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs 查看文档
@app.get("/")
async def root():
    return {"message": "request_header"}


@app.post("/items/")
async def create_item(item: Item):
    return item


# run: uvicorn request_header:app --reload
#   request_header: request_header.py 文件（一个 Python「模块」）。
#   app: 在 request_header.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
