# https://fastapi.tiangolo.com/zh/tutorial/static-files/
# 您可以使用 StaticFiles从目录中自动提供静态文件。
# 使用StaticFiles
# - 导入StaticFiles。
# - "挂载"(Mount) 一个 StaticFiles() 实例到一个指定路径。

# 什么是"挂载"(Mounting)
# "挂载" 表示在特定路径添加一个完全"独立的"应用，然后负责处理所有子路径。
# 这与使用APIRouter不同，因为安装的应用程序是完全独立的。OpenAPI和来自你主应用的文档不会包含已挂载应用的任何东西等等。

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "hello world"}


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
