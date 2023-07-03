# https://fastapi.tiangolo.com/zh/tutorial/dependencies/
import uvicorn
from fastapi import FastAPI, Depends


app = FastAPI()


# 编程中的「依赖注入」是声明代码（本文中为路径操作函数 ）运行所需的，或要使用的「依赖」的一种方式。
# 然后，由系统（本文中为 FastAPI）负责执行任意需要的逻辑，为代码提供这些依赖（「注入」依赖项）。
# 依赖注入常用于以下场景：
#   - 共享业务逻辑（复用相同的代码逻辑）
#   - 共享数据库连接
#   - 实现安全、验证、角色权限
#   - 等……
# 上述场景均可以使用依赖注入，将代码重复最小化。

# 要不要使用 async？
# FastAPI 调用依赖项的方式与路径操作函数一样，因此，定义依赖项函数，也要应用与路径操作函数相同的规则。
# 即，既可以使用异步的 async def，也可以使用普通的 def 定义依赖项。
# 在普通的 def 路径操作函数中，可以声明异步的 async def 依赖项；也可以在异步的 async def 路径操作函数中声明普通的 def 依赖项

# 本例中的依赖项预期接收如下参数：
#   - 类型为 str 的可选查询参数 q
#   - 类型为 int 的可选查询参数 skip，默认值是 0
#   - 类型为 int 的可选查询参数 limit，默认值是 100
# 然后，依赖项函数返回包含这些值的 dict
async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    return {"q": q, "skip": skip, "limit": limit}


# 与在路径操作函数参数中使用 Body、Query 的方式相同，声明依赖项需要使用 Depends 和一个新的参数
# 这里只能传给 Depends 一个参数。
# 且该参数必须是可调用对象，比如函数。
# 该函数接收的参数和路径操作函数的参数一样
# http://127.0.0.1:8001/docs
@app.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    commons["func"] = "items"
    return commons


# http://127.0.0.1:8001/docs
@app.get("/users")
async def read_users(commons: dict = Depends(common_parameters)):
    commons["func"] = "users"
    return commons


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
