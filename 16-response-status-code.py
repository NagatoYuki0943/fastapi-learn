# https://fastapi.tiangolo.com/zh/tutorial/response-status-code/
import uvicorn
from fastapi import FastAPI, status


app = FastAPI()


# 响应状态码
# 与指定响应模型的方式相同，你也可以在以下任意的路径操作中使用 status_code 参数来声明用于响应的 HTTP 状态码：
#   @app.get()
#   @app.post()
#   @app.put()
#   @app.delete()
#   等等。


# 在 HTTP 协议中，你将发送 3 位数的数字状态码作为响应的一部分。
# 这些状态码有一个识别它们的关联名称，但是重要的还是数字。
# 简而言之：
#   - 100 及以上状态码用于「消息」响应。你很少直接使用它们。具有这些状态代码的响应不能带有响应体。
#   - 200 及以上状态码用于「成功」响应。这些是你最常使用的。
#       - 200 是默认状态代码，它表示一切「正常」。
#       - 另一个例子会是 201，「已创建」。它通常在数据库中创建了一条新记录后使用。
#       - 一个特殊的例子是 204，「无内容」。此响应在没有内容返回给客户端时使用，因此该响应不能包含响应体。
#   - 300 及以上状态码用于「重定向」。具有这些状态码的响应可能有或者可能没有响应体，但 304「未修改」是个例外，该响应不得含有响应体。
#   - 400 及以上状态码用于「客户端错误」响应。这些可能是你第二常使用的类型。
#       - 一个例子是 404，用于「未找到」响应。
#       - 对于来自客户端的一般错误，你可以只使用 400。
#   - 500 及以上状态码用于服务器端错误。你几乎永远不会直接使用它们。当你的应用程序代码或服务器中的某些部分出现问题时，它将自动返回这些状态代码之一。


# http://127.0.0.1:8000/docs
@app.post("/items", response_model=dict[str, str], status_code=201)
async def create_item(name: str):
    return {"name": name}


# http://127.0.0.1:8000/docs
@app.post(
    "/items1", response_model=dict[str, str], status_code=status.HTTP_202_ACCEPTED
)
async def create_item1(name: str):
    return {"name": name}


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
