# FastAPI app 文件¶
# 假设你有一个像 更大的应用 中所描述的文件结构:

# .
# ├── app
# │   ├── __init__.py
# │   └── main.py

# 在 main.py 文件中你有一个 FastAPI app:

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
