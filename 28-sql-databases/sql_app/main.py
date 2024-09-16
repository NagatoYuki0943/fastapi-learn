# https://fastapi.tiangolo.com/zh/tutorial/sql-databases/
# 这些文档即将被更新。🎉
# 当前版本假设Pydantic v1和SQLAlchemy版本小于2。
# 新的文档将包括Pydantic v2以及 SQLModel（也是基于SQLAlchemy），一旦SQLModel更新为为使用Pydantic v2。


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# 创建数据库表
# 以非常简单的方式创建数据库表：
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 创建依赖项
# 现在使用我们在sql_app/database.py文件中创建的SessionLocal来创建依赖项。
# 我们需要每个请求有一个独立的数据库会话/连接（SessionLocal），在整个请求中使用相同的会话，然后在请求完成后关闭它。
# 然后将为下一个请求创建一个新会话。
# 为此，我们将创建一个包含yield的依赖项，正如前面关于Dependencies withyield的部分中所解释的那样。
# 我们的依赖项将创建一个新的 SQLAlchemy SessionLocal，它将在单个请求中使用，然后在请求完成后关闭它。
# Dependency
def get_db():
    db = SessionLocal()
    # 我们将SessionLocal()请求的创建和处理放在一个try块中。
    # 然后我们在finally块中关闭它。
    # 通过这种方式，我们确保数据库会话在请求后始终关闭。即使在处理请求时出现异常。
    try:
        yield db
    finally:
        db.close()


# *然后，当在路径操作函数*中使用依赖项时，我们使用Session，直接从 SQLAlchemy 导入的类型声明它。
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# 但是由于 SQLAlchemy 不具有await直接使用的兼容性，因此类似于：
# user = await db.query(User).first()
# ...相反，我们可以使用：
# user = db.query(User).first()
# 然后我们应该声明*路径操作函数*和不带 的依赖关系async def，只需使用普通的def，如下：
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
