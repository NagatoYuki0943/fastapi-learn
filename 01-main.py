# https://fastapi.tiangolo.com/zh/tutorial/first-steps/
import uvicorn
from fastapi import FastAPI


# pip install fastapi "uvicorn[standard]"
app = FastAPI()


# http://127.0.0.1:8001/
# http://127.0.0.1:8001/docs 查看文档
@app.get("/")
async def root():
    return {"message": "hello world"}


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
