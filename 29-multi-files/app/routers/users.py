# 假设专门用于处理用户逻辑的文件是位于 /app/routers/users.py 的子模块。
# 你希望将与用户相关的*路径操作*与其他代码分开，以使其井井有条。
# 但它仍然是同一 FastAPI 应用程序/web API 的一部分（它是同一「Python 包」的一部分）。
# 你可以使用 APIRouter 为该模块创建*路径操作*。

from fastapi import APIRouter


router = APIRouter()
# 可以使用它来声明*路径操作*。
# 使用方式与 FastAPI 类相同：
# 你可以将 APIRouter 视为一个「迷你 FastAPI」类。
# 所有相同的选项都得到支持。
# 所有相同的 parameters、responses、dependencies、tags 等等。


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
