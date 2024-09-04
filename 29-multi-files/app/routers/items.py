# 其他使用 APIRouter 的模块
# 假设你在位于 app/routers/items.py 的模块中还有专门用于处理应用程序中「项目」的端点。

# 你具有以下*路径操作*：

# /items/
# /items/{item_id}
# 这和 app/routers/users.py 的结构完全相同。

# 但是我们想变得更聪明并简化一些代码。

# 我们知道此模块中的所有*路径操作*都有相同的：

# 路径 prefix：/items。
# tags：（仅有一个 items 标签）。
# 额外的 responses。
# dependencies：它们都需要我们创建的 X-Token 依赖项。
# 因此，我们可以将其添加到 APIRouter 中，而不是将其添加到每个路径操作中。



from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


# 添加一些自定义的 tags、responses 和 dependencies¶
# 我们不打算在每个*路径操作*中添加前缀 /items 或 tags =["items"]，因为我们将它们添加到了 APIRouter 中。
# 但是我们仍然可以添加*更多*将会应用于特定的*路径操作*的 tags，以及一些特定于该*路径操作*的额外 responses：
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
