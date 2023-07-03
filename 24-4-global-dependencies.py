# https://fastapi.tiangolo.com/zh/tutorial/dependencies/global-dependencies/
import uvicorn
from fastapi import FastAPI, Depends, Depends, Header, HTTPException


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# 有时，我们要为整个应用添加依赖项。
# 通过与定义路径装饰器依赖项 类似的方式，可以把依赖项添加至整个 FastAPI 应用。
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


# run: uvicorn main:app --reload --port=8001
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    from pathlib import Path
    file = Path(__file__).stem  # get file name without suffix
    uvicorn.run(app=f"{file}:app", host="127.0.0.1", port=8001, reload=True)
