# 用Base类来创建 SQLAlchemy 模型
# 我们将使用我们之前创建的Base类来创建 SQLAlchemy 模型。


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    # 这个 __tablename__ 属性是用来告诉 SQLAlchemy 要在数据库中为每个模型使用的数据库表的名称。
    __tablename__ = "users"

    # 创建模型属性/列
    # 这些属性中的每一个都代表其相应数据库表中的一列。
    # 我们使用Column来表示 SQLAlchemy 中的默认值。
    # 我们传递一个 SQLAlchemy “类型”，如Integer、String和Boolean，它定义了数据库中的类型，作为参数。
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # 创建关系
    # 现在创建关系。
    # 为此，我们使用SQLAlchemy ORM提供的relationship。
    # 这将或多或少会成为一种“神奇”属性，其中表示该表与其他相关的表中的值。

    # 当访问 user 中的属性items时，如 中my_user.items，它将有一个ItemSQLAlchemy 模型列表（来自items表），这些模型具有指向users表中此记录的外键。
    # 当您访问my_user.items时，SQLAlchemy 实际上会从items表中的获取一批记录并在此处填充进去。
    # 同样，当访问 Item中的属性owner时，它将包含表中的UserSQLAlchemy 模型users。使用owner_id属性/列及其外键来了解要从users表中获取哪条记录。
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
