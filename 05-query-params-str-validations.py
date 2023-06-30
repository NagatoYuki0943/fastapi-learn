# https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/
import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()


# 查询参数 q 的类型为 str，默认值为 None，因此它是可选的
# http://127.0.0.1:8001/items/
# http://127.0.0.1:8001/items?q=what
@app.get("/items")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 将 Query 用作查询参数的默认值，并将它的 min_length, max_length, regex
# http://127.0.0.1:8001/items1/
# http://127.0.0.1:8001/items1?q=what
# http://127.0.0.1:8001/items1?q=fixedquery
@app.get("/items1")
async def read_items1(q: str | None = Query(default=None, min_length=3, max_length=10, regex=r"^\w{3, 50}$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 声明为必需参数 当我们不需要声明额外的校验或元数据时，只需不声明默认值就可以使 q 参数成为必需参数，例如
# http://127.0.0.1:8001/items2
# http://127.0.0.1:8001/items2?q=what
@app.get("/items2")
async def read_items2(q: str):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 或者使用 Query 且需要声明一个值是必需的时，只需不声明默认参数
# http://127.0.0.1:8001/items3
# http://127.0.0.1:8001/items3?q=what
@app.get("/items3")
async def read_items3(q: str = Query(min_length=3, max_length=10)): # Query(default=...)也是必须参数
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 查询参数列表 / 多个值
# 当你使用 Query 显式地定义查询参数时，你还可以声明它去接收一组值，或换句话来说，接收多个值。
# http://127.0.0.1:8001/items4?q=what&q=how
@app.get("/items4")
async def read_items4(q: list[str] = Query()):
    query_items = {"q": q}
    return query_items


# http://127.0.0.1:8001/items5
# http://127.0.0.1:8001/items5?q=what&q=how
@app.get("/items5")
async def read_items5(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# 声明变量的title和desc
# http://127.0.0.1:8001/items6
# http://127.0.0.1:8001/items6?q=what&q=how
@app.get("/items6")
async def read_items6(
    q: str | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
