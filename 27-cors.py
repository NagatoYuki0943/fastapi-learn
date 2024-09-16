# https://fastapi.tiangolo.com/zh/tutorial/middleware/
import uvicorn
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# 使用 CORSMiddleware
# 你可以在 FastAPI 应用中使用 CORSMiddleware 来配置它。
#   - 导入 CORSMiddleware。
#   - 创建一个允许的源列表（由字符串组成）。
#   - 将其作为「中间件」添加到你的 FastAPI 应用中。
# 使用 CORSMiddleware
# 你可以在 FastAPI 应用中使用 CORSMiddleware 来配置它。
#   - 导入 CORSMiddleware。
#   - 创建一个允许的源列表（由字符串组成）。
#   - 将其作为「中间件」添加到你的 FastAPI 应用中。

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


# CORSMiddleware 支持以下参数：
#   - allow_origins - 一个允许跨域请求的源列表。例如 ['https://example.org', 'https://www.example.org']。你可以使用 ['*'] 允许任何源。
#   - allow_origin_regex - 一个正则表达式字符串，匹配的源允许跨域请求。例如 'https://.*\.example\.org'。
#   - allow_methods - 一个允许跨域请求的 HTTP 方法列表。默认为 ['GET']。你可以使用 ['*'] 来允许所有标准方法。
#   - allow_headers - 一个允许跨域请求的 HTTP 请求头列表。默认为 []。你可以使用 ['*'] 允许所有的请求头。Accept、Accept-Language、Content-Language 以及 Content-Type 请求头总是允许 CORS 请求。
#   - allow_credentials - 指示跨域请求支持 cookies。默认是 False。另外，允许凭证时 allow_origins 不能设定为 ['*']，必须指定源。
#   - expose_headers - 指示可以被浏览器访问的响应头。默认为 []。
#   - max_age - 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600。
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# http://127.0.0.1:8000/docs
@app.get("/hello/{name}")
def home(name: str = Path(min_length=3)):
    return {"response": f"nihao,{name}"}


# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
