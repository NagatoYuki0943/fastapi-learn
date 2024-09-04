学习fastapi

# [FastAPI doc](https://fastapi.tiangolo.com/zh/)

# 安装

```sh
pip install fastapi
# 并且安装uvicorn来作为服务器
pip install "uvicorn[standard]"

# Email验证
pip install pydantic[email]

# 要使用表单，需预先安装 python-multipart
pip install python-multipart

# 接收上传文件，要预先安装 python-multipart
pip install python-multipart

# 进行测试，需要安装 httpx
pip install httpx
pip install pytest
```

# 简单运行

```
uvicorn main:app --reload
```

- `main`：`main.py` 文件（一个 Python「模块」）。
- `app`：在 `main.py` 文件中通过 `app = FastAPI()` 创建的对象。
- `--reload`：让服务器在更新代码后重新启动。仅在开发时使用该选项。