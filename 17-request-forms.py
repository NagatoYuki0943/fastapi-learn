# https://fastapi.tiangolo.com/zh/tutorial/request-forms/
# 要使用表单，需预先安装 python-multipart
# pip install python-multipart
from fastapi import FastAPI, Form, Body


app = FastAPI()


# 可在一个路径操作中声明多个 File 与 Form 参数，但不能同时声明要接收 JSON 的 Body 字段。设定 Body 后不会报错，而是强制使用 Form 发送数据
# 因为此时请求体的编码为 multipart/form-data，不是 application/json。
# 这不是 FastAPI 的问题，而是 HTTP 协议的规定。


# 创建表单（Form）参数的方式与 Body 和 Query 一样：
# 使用 Form 可以声明与 Body （及 Query、Path、Cookie）相同的元数据和验证
# Form 是直接继承自 Body 的类。
# 声明表单体要显式使用 Form ，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。
# 与 JSON 不同，HTML 表单（<form></form>）向服务器发送数据通常使用「特殊」的编码。
# FastAPI 要确保从正确的位置读取数据，而不是读取 JSON
# 表单数据的「媒体类型」编码一般为 application/x-www-form-urlencoded
# http://127.0.0.1:8000/docs
@app.post("/login")
async def login(
    username: str = Form(min_length=3),
    password: str = Form(min_length=3),
    json: str = Body(),  # 设定 Body 后不被报错，而是强制使用 Form 发送数据
):
    results = {"username": username, "json": json}
    return results


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
