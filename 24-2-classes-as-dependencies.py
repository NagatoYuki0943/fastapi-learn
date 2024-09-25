# https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
from fastapi import FastAPI, Depends


app = FastAPI()


# 类作为依赖项
# 在前面的例子中, 我们从依赖项 ("可依赖对象") 中返回了一个 dict:
# 但是后面我们在路径操作函数的参数 commons 中得到了一个 dict。
# 我们知道编辑器不能为 dict 提供很多支持(比如补全)，因为编辑器不知道 dict 的键和值类型。
# 对此，我们可以做的更好...


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# 什么构成了依赖项？
# 到目前为止，您看到的依赖项都被声明为函数。
# 但这并不是声明依赖项的唯一方法(尽管它可能是更常见的方法)。
# 关键因素是依赖项应该是 "可调用对象"。
# Python 中的 "可调用对象" 是指任何 Python 可以像函数一样 "调用" 的对象。
# 所以，如果你有一个对象 something (可能*不是*一个函数)，你可以 "调用" 它(执行它)，就像：
#     something()
# 或者
#     something(some_argument, some_keyword_argument="foo")
# 这就是 "可调用对象"。

# 类作为依赖项
# 您可能会注意到，要创建一个 Python 类的实例，您可以使用相同的语法。

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 注意用于创建类实例的 __init__ 方法
# ...它与我们以前的 common_parameters 具有相同的参数：
# 这些参数就是 FastAPI 用来 "处理" 依赖项的。
# 在两个例子下，都有：
#     - 一个可选的 q 查询参数，是 str 类型。
#     - 一个 skip 查询参数，是 int 类型，默认值为 0。
#     - 一个 limit 查询参数，是 int 类型，默认值为 100。


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# http://127.0.0.1:8000/docs
@app.get("/items1")
async def read_items1(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# 快捷方式
# FastAPI 为这些情况提供了一个快捷方式，在这些情况下，依赖项 明确地 是一个类，FastAPI 将 "调用" 它来创建类本身的一个实例。
# 对于这些特定的情况，您可以跟随以下操作：
# 不是写成这样：
#     commons: CommonQueryParams = Depends(CommonQueryParams)
# ...而是这样写:
#     commons: CommonQueryParams = Depends()
# 您声明依赖项作为参数的类型，并使用 Depends() 作为该函数的参数的 "默认" 值(在 = 之后)，而在 Depends() 中没有任何参数，而不是在 Depends(CommonQueryParams) 编写完整的类。
# ... FastAPI 会知道怎么处理。
@app.get("/items2/")
async def read_items2(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


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
