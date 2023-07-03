# https://fastapi.tiangolo.com/zh/tutorial/metadata/
import uvicorn
from fastapi import FastAPI


# OpenAPI URL
# 默认情况下，OpenAPI 模式服务于 /openapi.json。
# 但是你可以通过参数 openapi_url 对其进行配置。
# 例如，将其设置为服务于 /api/v1/openapi.json


app = FastAPI(openapi_url="/api/v1/openapi.json")


# http://127.0.0.1:8001/docs
@app.get("/items")
async def read_items():
    return [{"name": "Foo"}]


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
