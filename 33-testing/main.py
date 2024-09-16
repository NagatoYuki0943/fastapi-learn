# https://fastapi.tiangolo.com/zh/tutorial/testing/
# 使用 TestClient

# 导入 TestClient.
# 通过传入你的**FastAPI**应用创建一个 TestClient 。
# 创建名字以 test_ 开头的函数（这是标准的 pytest 约定）。
# 像使用 httpx 那样使用 TestClient 对象。
# 为你需要检查的地方用标准的Python表达式写个简单的 assert 语句（重申，标准的pytest）。


from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


# 注意测试函数是普通的 def，不是 async def。
# 还有client的调用也是普通的调用，不是用 await。
# 这让你可以直接使用 pytest 而不会遇到麻烦。
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# 运行
# pytest mian.py
# 默认运行 pytest 会执行 app 中的 test_ 开头的文件。
# 可以进入 app 目录，然后运行 pytest 。
