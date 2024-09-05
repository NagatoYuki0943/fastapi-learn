# https://fastapi.tiangolo.com/zh/tutorial/dependencies/dependencies-with-yield/
from typing import Annotated
import uvicorn
from fastapi import FastAPI, Depends, Depends, Header, HTTPException



app = FastAPI()


# 使用yield的依赖项
# FastAPI支持在完成后执行一些额外步骤的依赖项.
# 为此，你需要使用 yield 而不是 return，然后再编写这些额外的步骤（代码）。


class DBSession:
    def __init__(self) -> None:
        ...

    def close(self):
        ...


# 使用 yield 的数据库依赖项
# 例如，你可以使用这种方式创建一个数据库会话，并在完成后关闭它。

async def get_db():
    # 在发送响应之前，只会执行 yield 语句及之前的代码：
    db = DBSession()
    try:
        # 生成的值会注入到 路由函数 和其他依赖项中：
        yield db
    # yield 语句后面的代码会在创建响应后，发送响应前执行：
    finally:
        db.close()


# 包含 yield 和 try 的依赖项
# 如果在包含 yield 的依赖中使用 try 代码块，你会捕获到使用依赖时抛出的任何异常。
# 例如，如果某段代码在另一个依赖中或在 路由函数 中使数据库事务"回滚"或产生任何其他错误，你将会在依赖中捕获到异常。
# 因此，你可以使用 except SomeException 在依赖中捕获特定的异常。
# 同样，你也可以使用 finally 来确保退出步骤得到执行，无论是否存在异常。


class DepA:
    def __init__(self) -> None:
        ...

class DepB:
    def __init__(self) -> None:
        ...

def generate_dep_a():
    ...

def generate_dep_b():
    ...

def generate_dep_c():
    ...


# 使用 yield 的子依赖项
# 你可以声明任意数量和层级的树状依赖，而且它们中的任何一个或所有的都可以使用 yield。
# FastAPI 会确保每个带有 yield 的依赖中的"退出代码"按正确顺序运行。
# 例如，dependency_c 可以依赖于 dependency_b，而 dependency_b 则依赖于 dependency_a。
async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)


# 包含 yield 和 HTTPException 的依赖项¶
# 你可以使用带有 yield 的依赖项，并且可以包含 try 代码块用于捕获异常。
# 同样，你可以在 yield 之后的退出代码中抛出一个 HTTPException 或类似的异常。
data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item


# 包含 yield 和 except 的依赖项
# 如果你在包含 yield 的依赖项中使用 except 捕获了一个异常，然后你没有重新抛出该异常（或抛出一个新异常），与在普通的Python代码中相同，FastAPI不会注意到发生了异常。
class InternalError(Exception):
    pass


def get_username1():
    try:
        yield "Rick"
    except InternalError:
        print("Oops, we didn't raise again, Britney 😱")


@app.get("/items1/{item_id}")
def get_item1(item_id: str, username: Annotated[str, Depends(get_username1)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id


# 在包含 yield 和 except 的依赖项中一定要 raise
# 如果你在使用 yield 的依赖项中捕获到了一个异常，你应该再次抛出捕获到的异常，除非你抛出 HTTPException 或类似的其他异常，
# 你可以使用 raise 再次抛出捕获到的异常。
def get_username2():
    try:
        yield "Rick"
    except InternalError:
        print("We don't swallow the internal error here, we raise again 😎")
        raise   # 你可以使用 raise 再次抛出捕获到的异常。


@app.get("/items2/{item_id}")
def get_item2(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id


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
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
