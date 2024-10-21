# https://fastapi.tiangolo.com/zh/tutorial/request-forms-and-files/
# 接收上传文件，需预先安装 python-multipart
# pip install python-multipart
from fastapi import FastAPI, Path, File, Form, UploadFile, Query


app = FastAPI()

# 请求表单与文件
# 可在一个路径操作中声明多个 File 与 Form 参数，但不能同时声明要接收 JSON 的 Body 字段。设定 Body 后不被报错，而是强制使用 Form 发送数据
# 因为此时请求体的编码为 multipart/form-data，不是 application/json。
# 这不是 FastAPI 的问题，而是 HTTP 协议的规定。


# FastAPI 支持同时使用 File 和 Form 定义文件和表单字段。
# http://127.0.0.1:8000/docs
@app.post("/files/{itemsid}")
async def create_file(
    itemsid: int = Path(title="The ID of the item to set"),
    query: str = Query(),
    file: bytes | None = File(default=None),
    fileb: UploadFile | None = File(default=None),
    token: str = Form(min_length=3),
):
    results = {
        "itemsid": itemsid,
        "query": query,
        "token": token,
    }
    if file:
        results.update({"file_size": len(file)})
    if fileb:
        results["fileb_filename"] = fileb.filename
    print(results)
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
