# https://github.com/InternLM/lmdeploy/blob/main/lmdeploy/serve/openai/api_client.py

import os
import requests
import httpx
import aiohttp
import json


URL = "http://localhost:8000/v1/chat/completions"
URL = "https://api.moonshot.cn/v1/chat/completions"
URL = "https://api.siliconflow.cn/v1/chat/completions"


"""
设置临时变量

linux:
    export API_KEY="your token"

powershell:
    $env:API_KEY = "your token"
"""
api_key = os.getenv("API_KEY", "I AM AN API_KEY")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


# https://github.com/InternLM/lmdeploy/blob/main/lmdeploy/serve/openai/api_client.py
def requests_chat(data: dict):
    stream: bool = data["stream"]

    response: requests.Response = requests.post(
        URL, json=data, headers=headers, timeout=60, stream=stream
    )
    if not stream:
        yield response.json()
    else:
        chunk: bytes
        for chunk in response.iter_lines(
            chunk_size=8192, decode_unicode=False, delimiter=b"\n\n"
        ):
            if chunk:
                decoded: str = chunk.decode("utf-8")
                if decoded == "data: [DONE]":
                    continue
                elif decoded[:6] == "data: ":
                    yield json.loads(decoded[6:])


# help: https://www.perplexity.ai/search/wo-shi-yong-requests-shi-xian-q_g712n3SBObB5xH_2fnMQ
def httpx_sync_chat(data: dict):
    stream: bool = data["stream"]

    with httpx.Client() as client:
        if not stream:
            response: httpx.Response = client.post(
                URL, json=data, headers=headers, timeout=60
            )
            yield response.json()
        else:
            with client.stream(
                "POST", URL, json=data, headers=headers, timeout=60
            ) as response:
                chunk: str
                for chunk in response.iter_lines():
                    if chunk:
                        if chunk == "data: [DONE]":
                            continue
                        elif chunk[:6] == "data: ":
                            yield json.loads(chunk[6:])


async def httpx_async_chat(data: dict):
    stream: bool = data["stream"]

    async with httpx.AsyncClient() as client:
        if not stream:
            response: httpx.Response = await client.post(
                URL, json=data, headers=headers, timeout=60
            )
            yield response.json()
        else:
            async with client.stream(
                "POST", URL, json=data, headers=headers, timeout=60
            ) as response:
                chunk: str
                async for chunk in response.aiter_lines():
                    if chunk:
                        if chunk == "data: [DONE]":
                            continue
                        elif chunk[:6] == "data: ":
                            yield json.loads(chunk[6:])


# https://www.perplexity.ai/search/wo-shi-yong-aiohttpshi-xian-mo-6J27VL0aQsGNCykznLPlMw
async def aiohttp_async_chat(data: dict):
    stream: bool = data["stream"]

    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL, json=data, headers=headers, timeout=60
        ) as response:
            if not stream:
                data: str = await response.text("utf-8")
                yield json.loads(data)
            else:
                chunk: bytes
                buffer = ""
                async for chunk in response.content.iter_any():
                    if chunk:
                        buffer += chunk.decode("utf-8")
                        # openai api returns \n\n as a delimiter for messages
                        while "\n\n" in buffer:
                            message, buffer = buffer.split("\n\n", 1)
                            if message.startswith("data: "):
                                message = message[6:]
                                if message.strip() == "[DONE]":
                                    continue
                                yield json.loads(message)


async def async_chat(data: dict, func: callable):
    async for output in func(data):
        print(output)


if __name__ == "__main__":
    data = {
        # "model": "moonshot-v1-8k",
        "model": "internlm/internlm2_5-7b-chat",
        "messages": [{"role": "user", "content": "讲一个猫和老鼠的故事"}],
        "max_tokens": 1024,
        "n": 1,
        "temperature": 0.8,
        "top_p": 0.8,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "stream": False,
    }
    data_stream = data.copy()
    data_stream["stream"] = True

    for output in requests_chat(data):
        print(output)

    for output in requests_chat(data_stream):
        print(output)

    print("\n")

    for output in httpx_sync_chat(data):
        print(output)

    for output in httpx_sync_chat(data_stream):
        print(output)

    print("\n")

    import asyncio

    asyncio.run(async_chat(data, httpx_async_chat))
    asyncio.run(async_chat(data_stream, httpx_async_chat))

    print("\n")

    asyncio.run(async_chat(data, aiohttp_async_chat))
    asyncio.run(async_chat(data_stream, aiohttp_async_chat))