# https://fastapi.tiangolo.com/zh/tutorial/security/first-steps/
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


app = FastAPI()


# 假设**后端** API 在某个域。
# **前端**在另一个域，或（移动应用中）在同一个域的不同路径下。
# 并且，前端要使用后端的 username 与 password 验证用户身份。
# 固然，FastAPI 支持 OAuth2 身份验证。
# 但为了节省开发者的时间，不要只为了查找很少的内容，不得不阅读冗长的规范文档。
# 我们建议使用 FastAPI 的安全工具。

# 先安装 python-multipart。
# 安装命令： pip install python-multipart。
# 这是因为 OAuth2 使用**表单数据**发送 username 与 password。


# 密码流
# 现在，我们回过头来介绍这段代码的原理。
# Password 流**是 OAuth2 定义的，用于处理安全与身份验证的方式（**流）。
# OAuth2 的设计目标是为了让后端或 API 独立于服务器验证用户身份。
# 但在本例中，FastAPI 应用会处理 API 与身份验证。
# 下面，我们来看一下简化的运行流程：
# - 用户在前端输入 username 与password，并点击**回车**
# - （用户浏览器中运行的）前端把 username 与password 发送至 API 中指定的 URL（使用 tokenUrl="token" 声明）
# - API 检查 username 与password，并用令牌（Token） 响应（暂未实现此功能）：
# - 令牌只是用于验证用户的字符串
# - 一般来说，令牌会在一段时间后过期
#   - 过时后，用户要再次登录
#   - 这样一来，就算令牌被人窃取，风险也较低。因为它与永久密钥不同，**在绝大多数情况下**不会长期有效
# - 前端临时将令牌存储在某个位置
# - 用户点击前端，前往前端应用的其它部件
# - 前端需要从 API 中提取更多数据：
#   - 为指定的端点（Endpoint）进行身份验证
#   - 因此，用 API 验证身份时，要发送值为 Bearer + 令牌的请求头 Authorization
#   - 假如令牌为 foobar，Authorization 请求头就是： Bearer foobar

# FastAPI 的 OAuth2PasswordBearer
# FastAPI 提供了不同抽象级别的安全工具。
# 本例使用 OAuth2 的 Password 流以及 Bearer 令牌（Token）。为此要使用 OAuth2PasswordBearer 类。
# "说明"
#   Bearer 令牌不是唯一的选择。
#   但它是最适合这个用例的方案。
#   甚至可以说，它是适用于绝大多数用例的最佳方案，除非您是 OAuth2 的专家，知道为什么其它方案更合适。
#   本例中，FastAPI 还提供了构建工具。

# 创建 OAuth2PasswordBearer 的类实例时，要传递 tokenUrl 参数。该参数包含客户端（用户浏览器中运行的前端） 的 URL，用于发送 username 与 password，并获取令牌。
# 该参数不会创建端点或*路径操作*，但会声明客户端用来获取令牌的 URL /token 。此信息用于 OpenAPI 及 API 文档。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# "提示"
#   在此，tokenUrl="token" 指向的是暂未创建的相对 URL token。这个相对 URL 相当于 ./token。
#   因为使用的是相对 URL，如果 API 位于 https://example.com/，则指向 https://example.com/token。但如果 API 位于 https://example.com/api/v1/，它指向的就是https://example.com/api/v1/token。
#   因此，tokenUrl 应该是 API 根路径下的相对 URL。使用相对 URL 非常重要，可以确保应用在遇到使用代理这样的高级用例时，也能正常运行。


# 使用
# 接下来，使用 Depends 把 oauth2_scheme 传入依赖项。
# 该依赖项使用字符串（str）接收*路径操作函数*的参数 token 。
# http://127.0.0.1:8000/docs
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


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
