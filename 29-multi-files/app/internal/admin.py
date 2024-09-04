from fastapi import APIRouter

router = APIRouter()


# 现在，假设你的组织为你提供了 app/internal/admin.py 文件。
# 它包含一个带有一些由你的组织在多个项目之间共享的管理员*路径操作*的 APIRouter。
# 对于此示例，它将非常简单。但是假设由于它是与组织中的其他项目所共享的，因此我们无法对其进行修改，以及直接在 APIRouter 中添加 prefix、dependencies、tags 等：
@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
