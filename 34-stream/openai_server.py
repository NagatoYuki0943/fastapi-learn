# https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/api_server.py
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import numpy as np
import random


app = FastAPI()


# 与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。默认值为 None 的模型属性也是可选的。
class ChatRequest(BaseModel):
    model: str | None = Field(
        None,
        description="The model used for generating the response",
        examples=["gpt4o", "gpt4"],
    )
    messages: list[dict[str, str | list]] = Field(
        None,
        description="List of dictionaries containing the input text and the corresponding user id",
        examples=[
            [{"role": "user", "content": "你是谁?"}],
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "图片中有什么内容?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": "https://example.com/image.jpg"},
                        },
                    ],
                }
            ],
        ],
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


# -------------------- 非流式响应模型 --------------------#
class ChatCompletionMessage(BaseModel):
    content: str | None = Field(
        None,
        description="The input text of the user or assistant",
        examples=["你是谁?"],
    )
    # 允许添加额外字段
    references: list[str] | None = Field(
        None,
        description="The references text(s) used for generating the response",
        examples=[["book1", "book2"]],
    )
    role: str = Field(
        None,
        description="The role of the user or assistant",
        examples=["system", "user", "assistant"],
    )
    refusal: bool = Field(
        False,
        description="Whether the user or assistant refused to provide a response",
        examples=[False, True],
    )
    function_call: str | None = Field(
        None,
        description="The function call that the user or assistant made",
        examples=["ask_name", "ask_age", "ask_location"],
    )
    tool_calls: str | None = Field(
        None,
        description="The tool calls that the user or assistant made",
        examples=["weather", "calendar", "news"],
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


class ChatCompletionChoice(BaseModel):
    index: int = Field(
        None,
        description="The index of the choice",
        examples=[0, 1, 2],
    )
    finish_reason: str | None = Field(
        None,
        description="The reason for finishing the conversation",
        examples=[None, "stop"],
    )
    logprobs: list[float] | None = Field(
        None,
        description="The log probabilities of the choices",
        examples=[-1.3862943611198906, -1.3862943611198906, -1.3862943611198906],
    )
    message: ChatCompletionMessage | None = Field(
        None,
        description="The message generated by the model",
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


class CompletionUsage(BaseModel):
    prompt_tokens: int = Field(
        0,
        description="The number of tokens in the prompt",
        examples=[10],
    )
    completion_tokens: int = Field(
        0,
        description="The number of tokens in the completion",
        examples=[10],
    )
    total_tokens: int = Field(
        0,
        description="The total number of tokens generated",
        examples=[10],
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


class ChatCompletion(BaseModel):
    id: str | int | None = Field(
        None,
        description="The id of the conversation",
        examples=[123456, "abc123"],
    )
    choices: list[ChatCompletionChoice] = Field(
        [],
        description="The choices generated by the model",
    )
    created: int | float | None = Field(
        None,
        description="The timestamp when the conversation was created",
    )
    model: str | None = Field(
        None,
        description="The model used for generating the response",
        examples=["gpt4o", "gpt4"],
    )
    object: str = Field(
        "chat.completion",
        description="The object of the conversation",
        examples=["chat.completion"],
    )
    service_tier: str | None = Field(
        None,
        description="The service tier of the conversation",
        examples=["basic", "premium"],
    )
    system_fingerprint: str | None = Field(
        None,
        description="The system fingerprint of the conversation",
        examples=["1234567890abcdef"],
    )
    usage: CompletionUsage = Field(
        CompletionUsage(),
        description="The usage of the completion",
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


# -------------------- 非流式响应模型 --------------------#


# -------------------- 流式响应模型 --------------------#
class ChoiceDelta(ChatCompletionMessage): ...


class ChatCompletionChunkChoice(BaseModel):
    index: int = Field(
        None,
        description="The index of the choice",
        examples=[0, 1, 2],
    )
    finish_reason: str | None = Field(
        None,
        description="The reason for finishing the conversation",
        examples=[None, "stop"],
    )
    logprobs: list[float] | None = Field(
        None,
        description="The log probabilities of the choices",
        examples=[-1.3862943611198906, -1.3862943611198906, -1.3862943611198906],
    )
    delta: ChoiceDelta | None = Field(
        None,
        description="The message generated by the model",
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


class ChatCompletionChunk(BaseModel):
    id: str | int | None = Field(
        None,
        description="The id of the conversation",
        examples=[123456, "abc123"],
    )
    choices: list[ChatCompletionChunkChoice] = Field(
        [],
        description="The choices generated by the model",
    )
    created: int | float | None = Field(
        None,
        description="The timestamp when the conversation was created",
    )
    model: str | None = Field(
        None,
        description="The model used for generating the response",
        examples=["gpt4o", "gpt4"],
    )
    object: str = Field(
        "chat.completion.chunk",
        description="The object of the conversation",
        examples=["chat.completion.chunk"],
    )
    service_tier: str | None = Field(
        None,
        description="The service tier of the conversation",
        examples=["basic", "premium"],
    )
    system_fingerprint: str | None = Field(
        None,
        description="The system fingerprint of the conversation",
        examples=["1234567890abcdef"],
    )
    usage: CompletionUsage = Field(
        None,
        description="The usage of the completion",
    )

    def __repr__(self) -> str:
        return self.model_dump_json()


# -------------------- 流式响应模型 --------------------#


# 将请求体作为 JSON 读取
# 在函数内部，你可以直接访问模型对象的所有属性
# http://127.0.0.1:8000/docs
@app.post("/v1/chat/completions", response_model=ChatCompletion)
async def chat(request: ChatRequest):
    print("request: ", request)

    messages = request.messages
    print("messages: ", messages)

    if not messages or len(messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")

    role = messages[-1].get("role", "")
    if role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    content = messages[-1].get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="content is empty")
    content_len = len(content)

    number = str(np.random.randint(0, 100, 10))
    print(f"number: {number}")
    references = [f"book{i+1}" for i in np.random.randint(1, 5, 3)]

    session_id = random.getrandbits(64)

    # 流式响应
    if request.stream:

        async def generate():
            for i, n in enumerate(number):
                time.sleep(0.2)
                chat_completion_chunk = ChatCompletionChunk(
                    id=session_id,
                    choices=[
                        ChatCompletionChunkChoice(
                            index=0,
                            finish_reason=None,
                            delta=ChoiceDelta(
                                content=n,
                                role="assistant",
                            ),
                        )
                    ],
                    created=time.time(),
                    usage=CompletionUsage(
                        prompt_tokens=content_len,
                        completion_tokens=i + 1,
                        total_tokens=content_len + i + 1,
                    ),
                )
                print(chat_completion_chunk)
                # openai api returns \n\n as a delimiter for messages
                yield f"data: {chat_completion_chunk.model_dump_json()}\n\n"

            chat_completion_chunk = ChatCompletionChunk(
                id=session_id,
                choices=[
                    ChatCompletionChunkChoice(
                        index=0,
                        finish_reason="stop",
                        delta=ChoiceDelta(
                            references=references,
                        ),
                    )
                ],
                created=time.time(),
                usage=CompletionUsage(
                    prompt_tokens=content_len,
                    completion_tokens=len(number),
                    total_tokens=content_len + len(number),
                ),
            )
            print(chat_completion_chunk)
            # openai api returns \n\n as a delimiter for messages
            yield f"data: {chat_completion_chunk.model_dump_json()}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(generate())

    # 非流式响应
    chat_completion = ChatCompletion(
        id=session_id,
        choices=[
            ChatCompletionChoice(
                index=0,
                finish_reason="stop",
                message=ChatCompletionMessage(
                    content=number,
                    references=references,
                    role="assistant",
                ),
            ),
        ],
        created=time.time(),
        usage=CompletionUsage(
            prompt_tokens=content_len,
            completion_tokens=len(number),
            total_tokens=content_len + len(number),
        ),
    )
    print(chat_completion)
    return chat_completion


# run: uvicorn main:app --reload --host=0.0.0.0 --port=8000
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
