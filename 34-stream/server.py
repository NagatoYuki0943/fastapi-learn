# https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/api_server.py
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import numpy as np


app = FastAPI()


# 与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。默认值为 None 的模型属性也是可选的。
class ChatRequest(BaseModel):
    model: str | None = Field(
        None,
        description="The model used for generating the response",
        examples=["gpt4o", "gpt4"],
    )
    messages: list[dict[str, str]] = Field(
        None,
        description="List of dictionaries containing the input text and the corresponding user id",
        examples=[[{"role": "user", "content": "你是谁?"}]],
    )
    max_tokens: int = Field(
        1024, ge=1, le=2048, description="Maximum number of new tokens to generate"
    )
    n: int = Field(
        1,
        ge=1,
        le=10,
        description="Number of completions to generate for each prompt",
    )
    temperature: float = Field(
        0.8,
        ge=0.1,
        le=2.0,
        description="Sampling temperature (lower temperature results in less random completions",
    )
    top_p: float = Field(
        0.8,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling top-p (top-p sampling chooses from the smallest possible set of tokens whose cumulative probability mass exceeds the probability top_p)",
    )
    top_k: int = Field(
        50,
        ge=0,
        le=100,
        description="Top-k sampling chooses from the top k tokens with highest probability",
    )
    stream: bool = Field(
        False,
        description="Whether to stream the output or wait for the whole response before returning it",
    )


class Response(BaseModel):
    response: str = Field(
        None,
        description="Generated text response",
        examples=[
            "InternLM (书生·浦语) is a conversational language model that is developed by Shanghai AI Laboratory (上海人工智能实验室)."
        ],
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


# 将请求体作为 JSON 读取
# 在函数内部，你可以直接访问模型对象的所有属性
# http://127.0.0.1:8000/docs
@app.post("/chat", response_model=Response)
async def chat(request: ChatRequest):
    print(request)

    if not request.messages or len(request.messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")

    role = request.messages[-1].get("role", "")
    if role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    content = request.messages[-1].get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="content is empty")

    if request.stream:

        async def generate():
            for i in np.random.randint(0, 100, 10):
                time.sleep(0.2)
                response = Response(response=str(i))
                print(response)
                # openai api returns \n\n as a delimiter for messages
                yield response.model_dump_json() + "\n\n"

        return StreamingResponse(generate())

    number = str(np.random.randint(0, 100, 10))
    response = Response(response=number)
    print(response)
    return response


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
