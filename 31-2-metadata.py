# https://fastapi.tiangolo.com/zh/tutorial/metadata/
from fastapi import FastAPI


# 标签元数据
# 你也可以使用参数 openapi_tags，为用于分组路径操作的不同标签添加额外的元数据。
# 它接受一个列表，这个列表包含每个标签对应的一个字典。
# 每个字典可以包含：
# - name（必要）：一个 str，它与路径操作和 APIRouter 中使用的 tags 参数有相同的标签名。
# - description：一个用于简短描述标签的 str。它支持 Markdown 并且会在文档用户界面中显示。
# - externalDocs：一个描述外部文档的 dict：
#   - description：用于简短描述外部文档的 str。
#   - url（必要）：外部文档的 URL str。

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


app = FastAPI(openapi_tags=tags_metadata)


# tags和上面tags_metadata中匹配
# http://127.0.0.1:8000/docs
@app.get("/users", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


# http://127.0.0.1:8000/docs
@app.get("/items", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]


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
