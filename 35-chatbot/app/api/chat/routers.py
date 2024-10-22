# https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/api_server.py
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Annotated
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from ...core import Session
from ...models import UserDB, ModelDB, ConversationDB
from ...envs import ENVS

from ...dependencies import (
    verify_access_token,
    oauth2_scheme,
)


DEFAULT_MODEL = "gpt4o"


router = APIRouter()
# 可以使用它来声明*路径操作*。
# 使用方式与 FastAPI 类相同：
# 你可以将 APIRouter 视为一个「迷你 FastAPI」类。
# 所有相同的选项都得到支持。
# 所有相同的 parameters、responses、dependencies、tags 等等。


chatbot_config = ENVS.get("chatbot", {})
api_key: str = chatbot_config.get("api_key", "I AM AN API_KEY")
base_url: str = chatbot_config.get("base_url", "http://localhost:8000/v1/")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


# 创建数据库会话
session = Session()


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
    conversation_id: int | None = Field(
        None,
        description="The id of the conversation",
        examples=[
            123456,
        ],
    )


def save_conversation(user: UserDB, model: ModelDB, messages: list[dict[str, str]], input_tokens: int, output_tokens: int, conversation_id=None):
    conversation = session.query(ConversationDB).get(conversation_id) if conversation_id else None
    if conversation:
        conversation.messages = messages
        conversation.model = model
        conversation.input_tokens = input_tokens
        conversation.output_tokens = output_tokens
    else:
        conversation = ConversationDB(
            messages=messages,
            user=user,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
        session.add(conversation)
    session.commit()
    return conversation.id


# 将请求体作为 JSON 读取
# 在函数内部，你可以直接访问模型对象的所有属性
# http://127.0.0.1:8000/docs
@router.post("/v1/chat/completions", response_model=ChatCompletion)
async def chat(request: ChatRequest, token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = int(verify_access_token(token))
    print(user_id)

    # 验证用户和模型
    user: UserDB = session.query(UserDB).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    model_name = request.model or DEFAULT_MODEL
    model = session.query(ModelDB).filter(ModelDB.model_name == model_name).first()
    if not model:
        model = ModelDB(model_name=model_name)
        session.add(model)
        session.commit()

    print(request)
    if not request.messages or len(request.messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")

    role = request.messages[-1].get("role", "")
    if role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    query = request.messages[-1].get("content", "")
    if not query:
        raise HTTPException(status_code=400, detail="query is empty")

    chat_completion: ChatCompletion = client.chat.completions.create(
        messages=request.messages,
        model="internlm/internlm2_5-7b-chat",
        max_tokens=request.max_tokens,
        n=request.n,  # 为每条输入消息生成多少个结果，默认为 1
        presence_penalty=0.0,  # 存在惩罚，介于-2.0到2.0之间的数字。正值会根据新生成的词汇是否出现在文本中来进行惩罚，增加模型讨论新话题的可能性
        frequency_penalty=0.0,  # 频率惩罚，介于-2.0到2.0之间的数字。正值会根据新生成的词汇在文本中现有的频率来进行惩罚，减少模型一字不差重复同样话语的可能性
        stream=request.stream,  # 是否流式响应
        temperature=request.temperature,
        top_p=request.top_p,
    )

    # 流式响应
    if request.stream:
        async def generate():
            full_response = []
            for idx, chunk in enumerate(chat_completion):
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                response_str = chunk_message.content
                full_response.append(response_str)
                yield f"data: {chunk.model_dump_json()}\n\n"

            # 保存完整的对话到数据库
            full_response = "".join(full_response)
            messages: list[dict[str, str]] = request.messages + [{"role": "assistant", "content": full_response}]
            input_tokens = sum(len(message["content"]) for message in request.messages)
            output_tokens = len(full_response)
            save_conversation(user, model, messages, input_tokens, output_tokens, request.conversation_id)

            yield "data: [DONE]\n\n"

        return StreamingResponse(generate())

    # 非流式响应
    response_str = chat_completion.choices[0].message.content

    # 保存到数据库
    messages = request.messages + [{"role": "assistant", "content": response_str}]
    input_tokens = sum(len(message["content"]) for message in messages)
    output_tokens = len(response_str)
    save_conversation(user, model, messages, input_tokens, output_tokens, request.conversation_id)

    return chat_completion


# 与声明查询参数一样，包含默认值的模型属性是可选的，否则就是必选的。默认值为 None 的模型属性也是可选的。
class Messages(BaseModel):
    id: int = Field(
        None,
        description="The id of the conversation",
    )
    user_id: int | None = Field(
        None,
        description="The id of the user",
    )
    model: str | None = Field(
        None,
        description="The name of the model",
    )
    title: str | None = Field(
        None,
        description="The title of the conversation",
    )
    messages: list[dict[str, str]] | None = Field(
        None,
        description="List of dictionaries containing the input text and the corresponding user id",
        examples=[[{"role": "user", "content": "你是谁?"}]],
    )
    desc: str | None = Field(
        None,
        description="The description of the conversation",
    )


@router.get("/history", response_model=list[Messages])
async def history(
    token: Annotated[str, Depends(oauth2_scheme)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    user_id = int(verify_access_token(token))
    print(user_id)

    # 验证用户和模型
    user: UserDB = session.query(UserDB).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    # conversations: list[ConversationDB] = user.conversations
    conversations: list[ConversationDB] = (
        session.query(ConversationDB)
        .filter(ConversationDB.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not conversations:
        return []

    responses = []
    for conversation in conversations:
        responses.append(
            Messages(
                id=conversation.id,
                user_id=user_id,
                title=conversation.title,
                messages=conversation.messages,
                desc=conversation.desc,
                model=conversation.model.model_name,
            )
        )

    return responses
