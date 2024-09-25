# https://fastapi.tiangolo.com/zh/tutorial/background-tasks/
# 你可以定义在返回响应后运行的后台任务。
# 这对需要在请求之后执行的操作很有用，但客户端不必在接收响应之前等待操作完成。
# 包括这些例子：
# - 执行操作后发送的电子邮件通知：
#     - 由于连接到电子邮件服务器并发送电子邮件往往很“慢”（几秒钟），您可以立即返回响应并在后台发送电子邮件通知。
# - 处理数据：
#     - 例如，假设您收到的文件必须经过一个缓慢的过程，您可以返回一个"Accepted"(HTTP 202)响应并在后台处理它。
from typing import Annotated
from fastapi import BackgroundTasks, Depends, FastAPI


app = FastAPI()


# 创建一个任务函数
# 创建要作为后台任务运行的函数。
# 它只是一个可以接收参数的标准函数。
# 它可以是 async def 或普通的 def 函数，FastAPI 知道如何正确处理。
# 在这种情况下，任务函数将写入一个文件（模拟发送电子邮件）。
# 由于写操作不使用 async 和 await，我们用普通的 def 定义函数：
def write_notification(email: str, message=""):
    with open("30-log-1.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


# 在你的 路径操作函数 里，用 .add_task() 方法将任务函数传到 后台任务 对象中：
# .add_task() 接收以下参数：
# 在后台运行的任务函数(write_notification)。
# 应按顺序传递给任务函数的任意参数序列(email)。
# 应传递给任务函数的任意关键字参数(message="some notification")。
@app.post("/send-notification1/{email}")
async def send_notification1(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


def write_log(message: str):
    with open("30-log-2.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


# 依赖注入
# 使用 BackgroundTasks 也适用于依赖注入系统，你可以在多个级别声明 BackgroundTasks 类型的参数：在 路径操作函数 里，在依赖中(可依赖)，在子依赖中，等等。
# FastAPI 知道在每种情况下该做什么以及如何复用同一对象，因此所有后台任务被合并在一起并且随后在后台运行：
@app.post("/send-notification2/{email}")
async def send_notification2(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}


# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path
    import uvicorn

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
