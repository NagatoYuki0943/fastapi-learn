# https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
import uvicorn
from fastapi import FastAPI, Depends


app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 注意用于创建类实例的 __init__ 方法
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 10):
        self.q = q
        self.skip = skip
        self.limit = limit


# http://127.0.0.1:8001/docs
@app.get("/items")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
