# https://fastapi.tiangolo.com/zh/tutorial/metadata/
import uvicorn
from fastapi import FastAPI


# 标题、描述和版本
# 你可以设定：
# - Title：在 OpenAPI 和自动 API 文档用户界面中作为 API 的标题/名称使用。
# - Description：在 OpenAPI 和自动 API 文档用户界面中用作 API 的描述。
# - Version：API 版本，例如 v2 或者 2.5.0。
#   - 如果你之前的应用程序版本也使用 OpenAPI 会很有用。
description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# http://127.0.0.1:8001/docs
@app.get("/items")
async def read_items():
    return [{"name": "Katana"}]


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
