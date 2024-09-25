# https://fastapi.tiangolo.com/zh/tutorial/path-params/
from fastapi import FastAPI
from enum import Enum


# pip install fastapi "uvicorn[standard]"
app = FastAPI()


# 路径值设置默认值在下面,使用的 Enum
# http://127.0.0.1:8000/items/1  路径参数设置
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 顺序很重要
# 在创建路径操作时，你会发现有些情况下路径是固定的。
# 比如 /users/me，我们假设它用来获取关于当前用户的数据.
# 然后，你还可以使用路径 /users/{user_id} 来通过用户 ID 获取关于特定用户的数据。
# 由于路径操作是按顺序依次运行的，你需要确保路径 /users/me 声明在路径 /users/{user_id}之前
# http://127.0.0.1:8000/users/me
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# http://127.0.0.1:8000/users/10
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# 预设值
# 如果你有一个接收路径参数的路径操作，但你希望预先设定可能的有效参数值，则可以使用标准的 Python Enum 类型
class ModelName(str, Enum):
    lenet = "lenet"
    alexnet = "alexnet"
    resnet = "resnet"


# http://127.0.0.1:8000/models/lenet
# http://127.0.0.1:8000/models/alexnet
# http://127.0.0.1:8000/models/resnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    return {"model_name": model_name, "message": "Have some residuals"}


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
