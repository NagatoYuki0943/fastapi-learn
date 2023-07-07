# https://fastapi.tiangolo.com/zh/tutorial/request-files/
# 接收上传文件，需预先安装 python-multipart
# pip install python-multipart
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
import cv2
from pathlib import Path


app = FastAPI()


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


ALLOW_SUFFIXES = [".jpg", "jpeg", "png", "fig", "tiff", "webp"]
# 带有额外元数据的 UploadFile
# 您也可以将 File() 与 UploadFile 一起使用，例如，设置额外的元数据:
# http://127.0.0.1:8001/docs
@app.post("/uploadfile1")
async def create_upload_file1(
    file: UploadFile = File(description="A Pic"),
):
    # suffix
    filename = Path(file.filename)
    suffix = filename.suffix
    if suffix not in ALLOW_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=f"suffix must be in {ALLOW_SUFFIXES}",
        )

    contents = await file.read()                        # async read

    # 转化为numpy数组再保存
    array    = np.asarray(bytearray(contents))          # 转化为1维数组
    image    = cv2.imdecode(array, cv2.IMREAD_COLOR)    # 转换为图片
    cv2.imwrite("18-1.jpg", image)

    # 直接保存也可以
    # with open(filename, mode="wb") as f:
    #     f.write(contents)

    results  = {"filename": file.filename, "size": file.size, "type": file.content_type, "shape": image.shape}
    return results


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
