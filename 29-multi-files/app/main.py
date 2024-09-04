# https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/


# - app 目录包含了所有内容。并且它有一个空文件 app/__init__.py，因此它是一个「Python 包」（「Python 模块」的集合）：app。
# - 它包含一个 app/main.py 文件。由于它位于一个 Python 包（一个包含 __init__.py 文件的目录）中，因此它是该包的一个「模块」：app.main。
# - 还有一个 app/dependencies.py 文件，就像 app/main.py 一样，它是一个「模块」：app.dependencies。
# - 有一个子目录 app/routers/ 包含另一个 __init__.py 文件，因此它是一个「Python 子包」：app.routers。
# - 文件 app/routers/items.py 位于 app/routers/ 包中，因此它是一个子模块：app.routers.items。
# - 同样适用于 app/routers/users.py，它是另一个子模块：app.routers.users。
# - 还有一个子目录 app/internal/ 包含另一个 __init__.py 文件，因此它是又一个「Python 子包」：app.internal。
# - pp/internal/admin.py 是另一个子模块：app.internal.admin。
import uvicorn
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

# 可以声明全局依赖项，它会和每个 APIRouter 的依赖项组合在一起：
app = FastAPI(dependencies=[Depends(get_query_token)])


# 包含 users 和 items 的 APIRouter
app.include_router(users.router)
# 使用 app.include_router()，我们可以将每个 APIRouter 添加到主 FastAPI 应用程序中。
# 它将包含来自该路由器的所有路由作为其一部分。
app.include_router(items.router)

# 但是我们仍然希望在包含 APIRouter 时设置一个自定义的 prefix，以便其所有*路径操作*以 /admin 开头，我们希望使用本项目已经有的 dependencies 保护它，并且我们希望它包含自定义的 tags 和 responses。
# 我们可以通过将这些参数传递给 app.include_router() 来完成所有的声明，而不必修改原始的 APIRouter：
# 这样，原始的 APIRouter 将保持不变，因此我们仍然可以与组织中的其他项目共享相同的 app/internal/admin.py 文件。
# 结果是在我们的应用程序中，来自 admin 模块的每个*路径操作*都将具有：
# /admin 前缀 。
# admin 标签。
# get_token_header 依赖项。
# 418 响应。 🍵
# 但这只会影响我们应用中的 APIRouter，而不会影响使用它的任何其他代码。
# 因此，举例来说，其他项目能够以不同的身份认证方法使用相同的 APIRouter。
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


# http://127.0.0.1:8000/docs
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# 多次使用不同的 prefix 包含同一个路由器
# 你也可以在*同一*路由器上使用不同的前缀来多次使用 .include_router()。
# 在有些场景这可能有用，例如以不同的前缀公开同一个的 API，比方说 /api/v1 和 /api/latest。


