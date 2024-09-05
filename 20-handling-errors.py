# https://fastapi.tiangolo.com/zh/tutorial/handling-errors/
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
# FastAPI 提供了与 starlette.responses 相同的 fastapi.responses 作为快捷方式，但大部分响应操作都可以直接从 Starlette 导入。同理，Request 也是如此。


app = FastAPI()


# 处理错误
# 某些情况下，需要向客户端返回错误提示。
# 这里所谓的客户端包括前端浏览器、其他应用程序、物联网设备等。
# 需要向客户端返回错误提示的场景主要如下：
#   - 客户端没有执行操作的权限
#   - 客户端没有访问资源的权限
#   - 客户端要访问的项目不存在
#   - 等等 ...
# 遇到这些情况时，通常要返回 4XX（400 至 499）HTTP 状态码。
# 4XX 状态码与表示请求成功的 2XX（200 至 299） HTTP 状态码类似。
# 只不过，4XX 状态码表示客户端发生的错误。

# 使用 HTTPException
# 向客户端返回 HTTP 错误响应，可以使用 HTTPException。
# 导入 HTTPException
# 触发 HTTPException
# HTTPException 是额外包含了和 API 有关数据的常规 Python 异常。
# 因为是 Python 异常，所以不能 return，只能 raise。
# 如在调用路径操作函数里的工具函数时，触发了 HTTPException，FastAPI 就不再继续执行路径操作函数中的后续代码，而是立即终止请求，并把 HTTPException 的 HTTP 错误发送至客户端。
# 在介绍依赖项与安全的章节中，您可以了解更多用 raise 异常代替 return 值的优势。
# 本例中，客户端用 ID 请求的 item 不存在时，触发状态码为 404 的异常：
# 添加自定义响应头
# 有些场景下要为 HTTP 错误添加自定义响应头。例如，出于某些方面的安全需要。
# 一般情况下可能不会需要在代码中直接使用响应头。

items = {"foo": "The Foo Wrestlers"}

# http://127.0.0.1:8000/docs
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"}, # 添加自定义响应头
        )
    return {"item": items[item_id]}


# 安装自定义异常处理器
# 添加自定义处理器，要使用 Starlette 的异常工具。
# 假设要触发的自定义异常叫作 UnicornException。
# 且需要 FastAPI 实现全局处理该异常。
# 此时，可以用 @app.exception_handler() 添加自定义异常控制器：
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

# 请求 http://127.0.0.1:800/unicorns/yolo 时，路径操作会触发 UnicornException。
# 但该异常将会被 unicorn_exception_handler 处理。
# http://127.0.0.1:8000/docs
# http://127.0.0.1:800/unicorns/yolo
@app.get("/unicorns/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# 覆盖默认异常处理器
# FastAPI 自带了一些默认异常处理器。
# 触发 HTTPException 或请求无效数据时，这些处理器返回默认的 JSON 响应结果。
# 不过，也可以使用自定义处理器覆盖默认异常处理器。

# 覆盖请求验证异常
# 请求中包含无效数据时，FastAPI 内部会触发 RequestValidationError。
# 该异常也内置了默认异常处理器。
# 覆盖默认异常处理器时需要导入 RequestValidationError，并用 @app.excption_handler(RequestValidationError) 装饰异常处理器。
# 这样，异常处理器就可以接收 Request 与异常。

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items1/{item_id}")
async def read_item1(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}




# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv('PORT', 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv('HOST', '0.0.0.0')

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
