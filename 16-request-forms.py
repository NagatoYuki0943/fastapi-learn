# https://fastapi.tiangolo.com/zh/tutorial/request-forms/
# 要使用表单，需预先安装 python-multipart
# pip install python-multipart

import uvicorn
from fastapi import FastAPI, Form


app = FastAPI()


# 创建表单（Form）参数的方式与 Body 和 Query 一样：
# 使用 Form 可以声明与 Body （及 Query、Path、Cookie）相同的元数据和验证
# Form 是直接继承自 Body 的类。
# 声明表单体要显式使用 Form ，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。
# 与 JSON 不同，HTML 表单（<form></form>）向服务器发送数据通常使用「特殊」的编码。
# FastAPI 要确保从正确的位置读取数据，而不是读取 JSON
# 表单数据的「媒体类型」编码一般为 application/x-www-form-urlencoded
@app.post("/login")
async def login(username: str = Form(min_length=3), password: str = Form(min_length=3)):
    return {"username": username}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
