# https://fastapi.tiangolo.com/zh/tutorial/metadata/
import uvicorn
from fastapi import FastAPI


# 文档 URLs
# 你可以配置两个文档用户界面，包括：
# - Swagger UI：服务于 /docs。
#   - 可以使用参数 docs_url 设置它的 URL。
#   - 可以通过设置 docs_url=None 禁用它。
# - ReDoc：服务于 /redoc。
#   - 可以使用参数 redoc_url 设置它的 URL。
#   - 可以通过设置 redoc_url=None 禁用它。


app = FastAPI(docs_url="/documentation", redoc_url=None)


# http://127.0.0.1:8000/items
@app.get("/items")
async def read_items():
    return [{"name": "Foo"}]


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
