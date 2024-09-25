# https://fastapi.tiangolo.com/zh/tutorial/cookie-params/
from fastapi import FastAPI, Cookie


app = FastAPI()


# 声明 Cookie 参数的结构与声明 Query 参数和 Path 参数时相同
# http://127.0.0.1:8000/items
# http://127.0.0.1:8000/items?id=10
@app.get("/items")
async def read_items(id: str | None = Cookie(default=None)):
    return {"id": id}


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
