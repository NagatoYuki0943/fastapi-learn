# https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/
import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()


# 查询参数 q 的类型为 str，默认值为 None，因此它是可选的
# http://127.0.0.1:8000/items/
# http://127.0.0.1:8000/items?q=what
@app.get("/items")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 将 Query 用作查询参数的默认值，并将它的 min_length, max_length, regex
# http://127.0.0.1:8000/items1/
# http://127.0.0.1:8000/items1?q=what
# http://127.0.0.1:8000/items1?q=fixedquery
@app.get("/items1")
async def read_items1(
    q: str | None = Query(
        default=None, min_length=3, max_length=10, regex=r"^\w{3, 50}$"
    ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 声明为必需参数 当我们不需要声明额外的校验或元数据时，只需不声明默认值就可以使 q 参数成为必需参数，例如
# http://127.0.0.1:8000/items2
# http://127.0.0.1:8000/items2?q=what
@app.get("/items2")
async def read_items2(q: str):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 或者使用 Query 且需要声明一个值是必需的时，只需不声明默认参数
# http://127.0.0.1:8000/items3
# http://127.0.0.1:8000/items3?q=what
@app.get("/items3")
async def read_items3(
    q: str = Query(min_length=3, max_length=10),
):  # Query(default=...)也是必须参数
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用省略号(...)声明必需参数
# 有另一种方法可以显式的声明一个值是必需的，即将默认参数的默认值设为 ... ：
# Pydantic 和 FastAPI 使用...来显式的声明需要一个值。
@app.get("/items4/")
async def read_items4(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用None声明必需参数
# 你可以声明一个参数可以接收None值，但它仍然是必需的。这将强制客户端发送一个值，即使该值是None。
# 为此，你可以声明None是一个有效的类型，并仍然使用default=...：
@app.get("/items5/")
async def read_items5(q: str | None = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 查询参数列表 / 多个值
# 当你使用 Query 显式地定义查询参数时，你还可以声明它去接收一组值，或换句话来说，接收多个值。
# http://127.0.0.1:8000/items4?q=what&q=how
@app.get("/items6")
async def read_items6(q: list[str] = Query()):
    query_items = {"q": q}
    return query_items


# 具有默认值的查询参数列表 / 多个值¶
# 你还可以定义在没有任何给定值时的默认 list 值：
# http://127.0.0.1:8000/items5
# http://127.0.0.1:80700/items5?q=what&q=how
@app.get("/items7")
async def read_items7(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# 声明更多元数据
# http://127.0.0.1:8000/items6
# http://127.0.0.1:8000/items6?q=what&q=how
@app.get("/items8")
async def read_items8(
    q: str | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 别名参数
# 假设你想要查询参数为 item-query。
# 像下面这样：
#     http://127.0.0.1:8000/items/?item-query=foobaritems
# 但是 item-query 不是一个有效的 Python 变量名称。
# 最接近的有效名称是 item_query。
# 但是你仍然要求它在 URL 中必须是 item-query...
# 这时你可以用 alias 参数声明一个别名，该别名将用于在 URL 中查找查询参数值：
@app.get("/items9/")
async def read_items9(q: str | None = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 弃用参数
# 现在假设你不再喜欢此参数。
# 你不得不将其保留一段时间，因为有些客户端正在使用它，但你希望文档清楚地将其展示为已弃用。
# 那么将参数 deprecated=True 传入 Query：
@app.get("/items10/")
async def read_items10(
    q: str | None = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",
        deprecated=True,
    ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


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
