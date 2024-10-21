from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from ...envs import ENVS

database_env: dict = ENVS.get("database", {})

database_type = database_env.get("type", "mysql")
user = database_env.get("user", "root")
password = database_env.get("password", "root")
host = database_env.get("host", "localhost")
port = database_env.get("port", "3306")
database = database_env.get("database", "chatbot")

url = f"{database_type}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
