# 创建初始 Pydantic*模型*/模式
# 创建一个ItemBase和UserBasePydantic*模型*（或者我们说“schema”），他们拥有创建或读取数据时具有的共同属性。
# 然后创建一个继承自他们的ItemCreate和UserCreate，并添加创建时所需的其他数据（或属性）。
# 因此在创建时也应当有一个password属性。
# 但是为了安全起见，password不会出现在其他同类 Pydantic*模型*中，例如通过API读取一个用户数据时，它不应当包含在内。
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


# 创建初始 Pydantic*模型*/模式
# 创建一个ItemBase和UserBasePydantic*模型*（或者我们说“schema”），他们拥有创建或读取数据时具有的共同属性。
# 然后创建一个继承自他们的ItemCreate和UserCreate，并添加创建时所需的其他数据（或属性）。
# 因此在创建时也应当有一个password属性。
# 但是为了安全起见，password不会出现在其他同类 Pydantic*模型*中，例如通过API读取一个用户数据时，它不应当包含在内。
class ItemCreate(ItemBase):
    pass


# 创建用于读取/返回的Pydantic*模型/模式*
# 现在创建当从 API 返回数据时、将在读取数据时使用的Pydantic*模型（schemas）。*
# 例如，在创建一个项目之前，我们不知道分配给它的 ID 是什么，但是在读取它时（从 API 返回时）我们已经知道它的 ID。
# 同样，当读取用户时，我们现在可以声明items，将包含属于该用户的项目。
# 不仅是这些项目的 ID，还有我们在 Pydantic*模型*中定义的用于读取项目的所有数据：Item.
class Item(ItemBase):
    id: int
    owner_id: int

    # 使用 Pydantic 的orm_mode
    # 在用于查询的 Pydantic*模型*Item中User，添加一个内部Config类。
    # 此类Config用于为 Pydantic 提供配置。
    # 在Config类中，设置属性orm_mode = True。
    # 这样，而不是仅仅试图从dict上 id 中获取值，如下所示：
    #   id = data["id"]
    # 它还会尝试从属性中获取它，如：
    #   id = data.id
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
