# 在这个文件中，我们将编写可重用的函数用来与数据库中的数据进行交互。
# **CRUD**分别为：增加（**C**reate）、查询（**R**ead）、更改（**U**pdate）、删除（**D**elete），即增删改查。

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 创建数据
# 现在创建工具函数来创建数据。
# 它的步骤是：
#     使用您的数据创建一个 SQLAlchemy 模型*实例。*
#     使用add来将该实例对象添加到数据库会话。
#     使用commit来将更改提交到数据库（以便保存它们）。
#     使用refresh来刷新您的实例对象（以便它包含来自数据库的任何新数据，例如生成的 ID）。
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
