from fastapi import FastAPI
from .api import users_router, chat_router


# 可以声明全局依赖项，它会和每个 APIRouter 的依赖项组合在一起：
app = FastAPI()


app.include_router(users_router)
app.include_router(chat_router)


# http://127.0.0.1:8000/docs
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
