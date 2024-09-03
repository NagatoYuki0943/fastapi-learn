# https://fastapi.tiangolo.com/zh/tutorial/cookie-params/
import uvicorn
from fastapi import FastAPI, Header


app = FastAPI()


# 可以使用定义 Query, Path 和 Cookie 参数一样的方法定义 Header 参数
# http://127.0.0.1:8000/items
# http://127.0.0.1:8000/docs
@app.get("/items")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


# 自动转换
# Header 在 Path, Query 和 Cookie 提供的功能之上有一点额外的功能。
# 大多数标准的headers用 "连字符" 分隔，也称为 "减号" (-)。
# 但是像 user-agent 这样的变量在Python中是无效的。
# 因此, 默认情况下, Header 将把参数名称的字符从下划线 (_) 转换为连字符 (-) 来提取并记录 headers.
# 同时，HTTP headers 是大小写不敏感的，因此，因此可以使用标准Python样式(也称为 "snake_case")声明它们。
# 因此，您可以像通常在Python代码中那样使用 user_agent ，而不需要将首字母大写为 User_Agent 或类似的东西。
# 如果出于某些原因，你需要禁用下划线到连字符的自动转换，设置Header的参数 convert_underscores 为 False:
@app.get("/items1")
async def read_items1(
    strange_header: str | None = Header(default=None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# 重复的 headers
# 有可能收到重复的headers。这意味着，相同的header具有多个值。
# 您可以在类型声明中使用一个list来定义这些情况。
# 你可以通过一个Python list 的形式获得重复header的所有值。
# 比如, 为了声明一个 X-Token header 可以出现多次，你可以这样写：
@app.get("/items2")
async def read_items2(x_token: list[str] | None = Header(default=None)):
    return {"X-Token values": x_token}


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
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
