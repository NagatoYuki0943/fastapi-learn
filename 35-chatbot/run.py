# https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/#apirouter

import uvicorn
import os


# uvicorn app.main:app --reload --host=0.0.0.0 --port=8001
if __name__ == "__main__":
    # 从环境变量中获取端口号，默认为 8001
    port = int(os.getenv("PORT", 8001))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(app="app.main:app", host=host, port=port, reload=True)
