# https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/#apirouter

import uvicorn
import os


# uvicorn app.main:app --reload
if __name__ == "__main__":
    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv("PORT", 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(app="app.main:app", host=host, port=port, reload=True)
