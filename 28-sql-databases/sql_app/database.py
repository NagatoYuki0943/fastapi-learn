from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 为 SQLAlchemy 定义数据库 URL地址
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/test"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)
# connect_args={"check_same_thread": False}
# ...仅用于SQLite，在其他数据库不需要它。


# 创建一个SessionLocal类
# 每个SessionLocal类的实例都会是一个数据库会话。当然该类本身还不是数据库会话。
# 但是一旦我们创建了一个SessionLocal类的实例，这个实例将是实际的数据库会话。
# 我们将它命名为SessionLocal是为了将它与我们从 SQLAlchemy 导入的Session区别开来。
# 稍后我们将使用Session（从 SQLAlchemy 导入的那个）。
# 要创建SessionLocal类，请使用函数sessionmaker：
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建一个Base类
# 现在我们将使用declarative_base()返回一个类。
# 稍后我们将继承这个类，来创建每个数据库模型或类（ORM 模型）：
Base = declarative_base()
