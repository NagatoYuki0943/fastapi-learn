# https://fastapi.tiangolo.com/zh/tutorial/dependencies/sub-dependencies/
from fastapi import FastAPI, Depends, Cookie


app = FastAPI()


# 子依赖项
# FastAPI 支持创建含子依赖项的依赖项。
# 并且，可以按需声明任意深度的子依赖项嵌套层级。
# FastAPI 负责处理解析不同深度的子依赖项。


# 第一层依赖项
# 这段代码声明了类型为 str 的可选查询参数 q，然后返回这个查询参数。
# 这个函数很简单（不过也没什么用），但却有助于让我们专注于了解子依赖项的工作方式。
def query_extractor(q: str | None = None):
    return q


# 第二层依赖项
# 接下来，创建另一个依赖项函数，并同时用该依赖项自身再声明一个依赖项（所以这也是一个「依赖项」）：
# 这里重点说明一下声明的参数：
#   - 尽管该函数自身是依赖项，但还声明了另一个依赖项（它「依赖」于其他对象）
#       - 该函数依赖 query_extractor, 并把 query_extractor 的返回值赋给参数 q
#   - 同时，该函数还声明了类型是 str 的可选 cookie（last_query）
#       - 用户未提供查询参数 q 时，则使用上次使用后保存在 cookie 中的查询
def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: str | None = Cookie(default=None),
):
    if not q:
        return last_query
    return q


# http://127.0.0.1:8000/docs
@app.get("/items")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


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
