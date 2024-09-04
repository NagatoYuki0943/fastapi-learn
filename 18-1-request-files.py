# https://fastapi.tiangolo.com/zh/tutorial/request-files/
# 接收上传文件，需预先安装 python-multipart
# pip install python-multipart
import uvicorn
from fastapi import FastAPI, File, UploadFile


app = FastAPI()


# 创建文件（File）参数的方式与 Body 和 Form 一样
# File 是直接继承自 Form 的类
# 声明文件体必须使用 File，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。
# 文件作为「表单数据」上传。
# 如果把路径操作函数参数的类型声明为 bytes，FastAPI 将以 bytes 形式读取和接收文件内容。
# 这种方式把文件的所有内容都存储在内存里，适用于小型文件。
# 不过，很多情况下，UploadFile 更好用。
# http://127.0.0.1:8000/docs
@app.post("/files")
async def create_file(file: bytes = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


# UploadFile 与 bytes 相比有更多优势：
#   - 使用 spooled 文件：
#       - 存储在内存的文件超出最大上限时，FastAPI 会把文件存入磁盘；
#   - 这种方式更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存；
#   - 可获取上传文件的元数据；
#   - 自带 file-like async 接口；
#   - 暴露的 Python SpooledTemporaryFile 对象，可直接传递给其他预期「file-like」对象的库。

# UploadFile
#   - UploadFile 的属性如下：
#       - filename：上传文件名字符串（str），例如， myimage.jpg；
#       - content_type：内容类型（MIME 类型 / 媒体类型）字符串（str），例如，image/jpeg；
#       - file： SpooledTemporaryFile（ file-like 对象）。其实就是 Python文件，可直接传递给其他预期 file-like 对象的函数或支持库。
#   - UploadFile 支持以下 async 方法，（使用内部 SpooledTemporaryFile）可调用相应的文件方法。
#       - write(data)：把 data （str 或 bytes）写入文件；
#       - read(size)：按指定数量的字节或字符（size (int)）读取文件内容；
#       - seek(offset)：移动至文件 offset （int）字节处的位置；
#           - 例如，await myfile.seek(0) 移动到文件开头；
#           - 执行 await myfile.read() 后，需再次读取已读取内容时，这种方法特别好用；
#       - close()：关闭文件
# 因为上述方法都是 async 方法，要搭配「await」使用。
# http://127.0.0.1:8000/docs
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No file sent"}
    else:
        contents = await file.read()    # async
        # contents = myfile.file.read() # sync
        results = {"filename": file.filename, "size": file.size, "type": file.content_type}
        print(file.headers)
        print(results)
        return results


# 带有额外元数据的 UploadFile
# 您也可以将 File() 与 UploadFile 一起使用，例如，设置额外的元数据:
# http://127.0.0.1:8000/docs
@app.post("/uploadfile1")
async def create_upload_file1(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    results = {"filename": file.filename, "size": file.size, "type": file.content_type}
    print(file.headers)
    print(results)
    return results


# 多文件上传
# FastAPI 支持同时上传多个文件。
# 可用同一个「表单字段」发送含多个文件的「表单数据」。
# 上传多个文件时，要声明含 bytes 或 UploadFile 的列表（List）
# http://127.0.0.1:8000/docs
@app.post("/mulltifiles")
async def mulltifiles(
    files: list[bytes] = File(description="Multiple files as bytes")
):
    results = {"file_sizes": [len(file) for file in files]}
    print(results)
    return results


# http://127.0.0.1:8000/docs
@app.post("/mulltifiles1")
async def mulltifiles1(
    files: list[UploadFile] = File(description="Multiple files as UploadFile")
):
    results = {"filenames": [file.filename for file in files]}
    print(results)
    return results


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
