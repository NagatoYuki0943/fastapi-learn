# https://fastapi.tiangolo.com/zh/tutorial/request-forms-and-files/
# 接收上传文件，需预先安装 python-multipart
# pip install python-multipart
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, Body, Query


app = FastAPI()


# 可在一个路径操作中声明多个 File 与 Form 参数，但不能同时声明要接收 JSON 的 Body 字段。设定 Body 后不被报错，而是强制使用 Form 发送数据
# 因为此时请求体的编码为 multipart/form-data，不是 application/json。
# 这不是 FastAPI 的问题，而是 HTTP 协议的规定。

# FastAPI 支持同时使用 File 和 Form 定义文件和表单字段。
# http://127.0.0.1:8001/docs
@app.post("/files/{itemsid}")
async def create_file(
    itemsid: int,
    query: str = Query(),
    file: bytes = File(),
    token: str = Form(min_length=3),
    fileb: UploadFile = File(),
):
    results = {
        "itemsid": itemsid,
        "query": query,
        "file_size": len(file),
        "fileb_filename": fileb.filename,
        "token": token,
    }
    print(results)
    return results


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
