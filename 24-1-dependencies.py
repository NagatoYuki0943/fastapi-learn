# https://fastapi.tiangolo.com/zh/tutorial/dependencies/
import uvicorn
from fastapi import FastAPI, Depends


app = FastAPI()


# 依赖项
# FastAPI 提供了简单易用，但功能强大的**依赖注入**系统。
# 这个依赖系统设计的简单易用，可以让开发人员轻松地把组件集成至 FastAPI。

# 什么是依赖注入
# 编程中的「依赖注入」是声明代码（本文中为路径操作函数 ）运行所需的，或要使用的「依赖」的一种方式。
# 然后，由系统（本文中为 FastAPI）负责执行任意需要的逻辑，为代码提供这些依赖（「注入」依赖项）。
# 依赖注入常用于以下场景：
#   - 共享业务逻辑（复用相同的代码逻辑）
#   - 共享数据库连接
#   - 实现安全、验证、角色权限
#   - 等……
# 上述场景均可以使用依赖注入，将代码重复最小化。


# 创建依赖项
# 首先，要关注的是依赖项。
# 依赖项就是一个函数，且可以使用与*路径操作函数*相同的参数：
async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    return {"q": q, "skip": skip, "limit": limit}


# 大功告成。
# 只用了**2 行**代码。
# 依赖项函数的形式和结构与*路径操作函数*一样。
# 因此，可以把依赖项当作没有「装饰器」（即，没有 @app.get("/some-path") ）的路径操作函数。
# 依赖项可以返回各种内容。
# 本例中的依赖项预期接收如下参数：
#     - 类型为 str 的可选查询参数 q
#     - 类型为 int 的可选查询参数 skip，默认值是 0
#     - 类型为 int 的可选查询参数 limit，默认值是 100
# 然后，依赖项函数返回包含这些值的 dict。


# 与在路径操作函数参数中使用 Body、Query 的方式相同，声明依赖项需要使用 Depends 和一个新的参数
# 这里只能传给 Depends 一个参数。
# 且该参数必须是可调用对象，比如函数。
# 该函数接收的参数和路径操作函数的参数一样
# http://127.0.0.1:8000/docs
@app.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    commons["func"] = "items"
    return commons


# 虽然，在路径操作函数的参数中使用 Depends 的方式与 Body、Query 相同，但 Depends 的工作方式略有不同。
# 这里只能传给 Depends 一个参数。
# 且该参数必须是可调用对象，比如函数。
# 该函数接收的参数和*路径操作函数*的参数一样。

# 接收到新的请求时，FastAPI 执行如下操作：
#     - 用正确的参数调用依赖项函数（「可依赖项」）
#     - 获取函数返回的结果
#     - 把函数返回的结果赋值给*路径操作函数*的参数


# http://127.0.0.1:8000/docs
@app.get("/users")
async def read_users(commons: dict = Depends(common_parameters)):
    commons["func"] = "users"
    return commons


# 要不要使用 async？
# FastAPI 调用依赖项的方式与*路径操作函数*一样，因此，定义依赖项函数，也要应用与路径操作函数相同的规则。
# 即，既可以使用异步的 async def，也可以使用普通的 def 定义依赖项。
# 在普通的 def *路径操作函数*中，可以声明异步的 async def 依赖项；也可以在异步的 async def *路径操作函数*中声明普通的 def 依赖项。


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
