# https://fastapi.tiangolo.com/zh/tutorial/query-params/
import uvicorn
from fastapi import FastAPI


app = FastAPI()


# 询字符串是键值对的集合，这些键值对位于 URL 的 ？ 之后，并以 & 符号分隔
# 查询参数不是路径的固定部分，因此它们可以是可选的，并且可以有默认值
# 通过同样的方式，你可以将它们的默认值设置为 None 来声明可选查询参数
# 如果想让一个查询参数成为必需的，不声明任何默认值就可以
# http://127.0.0.1:8001/query                   有默认值,可以这样用
# http://127.0.0.1:8001/query?skip=2&limit=20
@app.get("/query")
async def search(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# 路径参数 + 查询参数
# http://127.0.0.1:8001/search/a                用默认值
# http://127.0.0.1:8001/search/a?skip=2&limit=10
@app.get("/search/{search}")
async def search(search: str, skip: int = 0, limit: int = 10):
    return {"search": search, "skip": skip, "limit": limit}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
