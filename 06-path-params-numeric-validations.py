# https://fastapi.tiangolo.com/zh/tutorial/path-params-numeric-validations/
from fastapi import FastAPI, Path, Query


app = FastAPI()


# 使用 Path 为路径参数声明相同类型的校验和元数据
# 路径参数总是必需的，因为它必须是路径的一部分
# http://127.0.0.1:8000/items/2/
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
):
    results = {"item_id": item_id}
    return results


# 按需对参数排序
# 假设你想要声明一个必需的 str 类型查询参数 q。而且你不需要为该参数声明任何其他内容，所以实际上你并不需要使用 Query。
# 但是你仍然需要使用 Path 来声明路径参数 item_id。
# 如果你将带有「默认值」的参数放在没有「默认值」的参数之前，Python 将会报错。
# 你可以对其重新排序，并将不带默认值的值（查询参数 q）放到最前面。
# 对 FastAPI 来说这无关紧要。它将通过参数的名称、类型和默认值声明（Query、Path 等）来检测参数，而不在乎参数的顺序。
# http://127.0.0.1:8000/items1/2?q=what
@app.get("/items1/{item_id}")
async def read_items1(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 按需对参数排序的技巧
# 如果你想不使用 Query 声明没有默认值的查询参数 q，同时使用 Path 声明路径参数 item_id，并使它们的顺序与上面不同，Python 对此有一些特殊的语法。
# 传递 * 作为函数的第一个参数。
# Python 不会对该 * 做任何事情，但是它将知道之后的所有参数都应作为关键字参数（键值对），也被称为 kwargs，来调用。即使它们没有默认值。
@app.get("/items2/{item_id}")
async def read_items2(
    *, item_id: int = Path(title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 数值校验：大于等于
# 使用 Query 和 Path（以及你将在后面看到的其他类）可以声明字符串约束，但也可以声明数值约束。
# 像下面这样，添加 ge=1 后，item_id 将必须是一个大于（greater than）或等于（equal）1 的整数。
#   gt：大于（greater than）
#   ge：大于等于（greater than or equal）
#   lt：大于（less than）
#   le：小于等于（less than or equal）
# http://127.0.0.1:8000/items3/0
# http://127.0.0.1:8000/items3/1
# http://127.0.0.1:8000/items3/2
# http://127.0.0.1:8000/items3/4
@app.get("/items3/{item_id}")
async def read_items3(
    item_id: int = Path(title="The ID of the item to get", ge=1, lt=4),
):
    results = {"item_id": item_id}
    return results


# 数值校验：浮点数、大于和小于
# 数值校验同样适用于 float 值。
# 能够声明 gt 而不仅仅是 ge 在这个前提下变得重要起来。例如，你可以要求一个值必须大于 0，即使它小于 1。
# 因此，0.5 将是有效值。但是 0.0或 0 不是。
# 对于 lt 也是一样的。
# http://127.0.0.1:8000/items4/1?size=0
# http://127.0.0.1:8000/items4/1?size=0.5
# http://127.0.0.1:8000/items4/1?size=10.5
@app.get("/items4/{item_id}")
async def read_items4(
    item_id: int = Path(title="The ID of the item to get", ge=1, lt=4),
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if size:
        results.update({"size": size})
    return results


# run: uvicorn main:app --reload --host=0.0.0.0 --port=8000
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
