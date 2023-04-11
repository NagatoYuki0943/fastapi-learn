from fastapi import FastAPI

# pip install fastapi "uvicorn[standard]"
app = FastAPI()


# base
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs 查看文档
@app.get("/")
async def root():
    return {"message": "hello world"}


# 路径参数  https://fastapi.tiangolo.com/zh/tutorial/path-params/
# http://127.0.0.1:8000/items/1  路径参数设置默认值无效
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 查询参数  https://fastapi.tiangolo.com/zh/tutorial/query-params/
# 询字符串是键值对的集合，这些键值对位于 URL 的 ？ 之后，并以 & 符号分隔
# 查询参数不是路径的固定部分，因此它们可以是可选的，并且可以有默认值
# 通过同样的方式，你可以将它们的默认值设置为 None 来声明可选查询参数
# 如果想让一个查询参数成为必需的，不声明任何默认值就可以
# http://127.0.0.1:8000/query                   有默认值,可以这样用
# http://127.0.0.1:8000/query?skip=2&limit=10
@app.get("/query")
async def search(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# 路径参数 + 查询参数
# http://127.0.0.1:8000/search/1                 用默认值
# http://127.0.0.1:8000/search/1?skip=2&limit=10
@app.get("/search/{search}")
async def search(search: int, skip: int = 0, limit: int = 10):
    return {"search": search, "skip": skip, "limit": limit}



# run: uvicorn main:app --reload
#   main: main.py 文件（一个 Python「模块」）。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
