# 测试文件
# 然后你会有一个包含测试的文件 test_main.py 。app可以像Python包那样存在（一样是目录，但有个 __init__.py 文件）：


from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# 默认运行 pytest 会执行 app 中的 test_ 开头的文件。
# 可以进入 app 目录，然后运行 pytest 。
