# https://fastapi.tiangolo.com/zh/tutorial/debugging/
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    import uvicorn

    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app, host="0.0.0.0", port=8000)
