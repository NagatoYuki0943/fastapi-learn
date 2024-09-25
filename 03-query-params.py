# https://fastapi.tiangolo.com/zh/tutorial/query-params/
from fastapi import FastAPI


app = FastAPI()


# ** 声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数。 **


# 查询字符串是键值对的集合，这些键值对位于 URL 的 ? 之后，并以 & 符号分隔
# 查询参数不是路径的固定部分，因此它们可以是可选的，并且可以有默认值
# 通过同样的方式，你可以将它们的默认值设置为 None 来声明可选查询参数
# 如果想让一个查询参数成为必需的，不声明任何默认值就可以
# http://127.0.0.1:8000/query                   有默认值,可以这样用
# http://127.0.0.1:8000/query?skip=2&limit=20
@app.get("/query")
async def query(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# 路径参数 + 查询参数
# http://127.0.0.1:8000/search/a                用默认值
# http://127.0.0.1:8000/search/a?skip=2&limit=10
@app.get("/search/{search}")
async def search(search: str, skip: int = 0, limit: int = 10):
    return {"search": search, "skip": skip, "limit": limit}


# 查询参数类型转换
# 参数还可以声明为 bool 类型，FastAPI 会自动转换参数类型：
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=0
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=False
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=false
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=off
# http://127.0.0.1:8000/items/foo?short=yes
# http://127.0.0.1:8000/items/foo?short=no
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# FastAPI 可以识别同时声明的多个路径参数和查询参数。
# 而且声明查询参数的顺序并不重要。
# http://127.0.0.1:8000/users/3/items/foo?short=1
# http://127.0.0.1:8000/users/3/items/foo?short=True&q=what
# http://127.0.0.1:8000/users/3/items/foo?short=no&q=how
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 必选查询参数
# 为不是路径参数的参数声明默认值（至此，仅有查询参数），该参数就**不是必选**的了。
# 如果只想把参数设为**可选**，但又不想指定参数的值，则要把默认值设为 None。
# 如果要把查询参数设置为**必选**，就不要声明默认值：
# http://127.0.0.1:8000/items2/4            错误
# http://127.0.0.1:8000/items2/4?needy=what   正确
# http://127.0.0.1:8000/items2/4?needy=what&skip=2&limit=20
@app.get("/items2/{item_id}")
async def read_item_with_needy(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


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
