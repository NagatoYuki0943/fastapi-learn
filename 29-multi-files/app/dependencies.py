# 依赖项
# 我们了解到我们将需要一些在应用程序的好几个地方所使用的依赖项。
# 因此，我们将它们放在它们自己的 dependencies 模块（app/dependencies.py）中。
# 现在我们将使用一个简单的依赖项来读取一个自定义的 X-Token 请求首部：


from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")



async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

