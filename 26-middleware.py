# https://fastapi.tiangolo.com/zh/tutorial/middleware/
import uvicorn
import time
from fastapi import FastAPI, Request, Path


app = FastAPI()


# "中间件"是一个函数,它在每个请求被特定的路径操作处理之前,以及在每个响应返回之前工作.
# - 它接收你的应用程序的每一个请求.
# - 然后它可以对这个请求做一些事情或者执行任何需要的代码.
# - 然后它将请求传递给应用程序的其他部分 (通过某种路径操作).
# - 然后它获取应用程序生产的响应 (通过某种路径操作).
# - 它可以对该响应做些什么或者执行任何需要的代码.
# - 然后它返回这个 响应.

# 如果你使用了 yield 关键字依赖, 依赖中的退出代码将在执行中间件后执行.
# 如果有任何后台任务(稍后记录), 它们将在执行中间件后运行.


# 中间件参数接收如下参数:
# - request.
# - 一个函数 call_next 它将接收 request 作为参数.
#   - 这个函数将 request 传递给相应的 路径操作.
#   - 然后它将返回由相应的路径操作生成的 response.
# - 然后你可以在返回 response 前进一步修改它.


# 可以添加自定义请求头 X-Process-Time 包含以秒为单位的接收请求和生成响应的时间:
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# http://127.0.0.1:8000/docs
@app.get("/hello/{name}")
def home(name: str = Path(min_length=3)):
    return {"response": f"nihao,{name}"}


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
