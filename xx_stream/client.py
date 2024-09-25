import requests
import httpx
import json


URL = "http://localhost:8000/chat"


def requests_chat(data: dict):
    stream = data["stream"]
    response: requests.Response = requests.post(URL, json=data, stream=stream)
    for chunk in response.iter_lines(
        chunk_size=8192, decode_unicode=False, delimiter=b"\n"
    ):
        if chunk:
            decoded = chunk.decode("utf-8")
            output = json.loads(decoded)
            yield output


def httpx_sync_chat(data: dict):
    stream = data["stream"]
    with httpx.Client() as client:
        if not stream:
            response: httpx.Response = client.post(URL, json=data)
            yield response.json()
        else:
            with client.stream("POST", URL, json=data) as response:
                chunk: str
                for chunk in response.iter_lines():
                    if chunk:
                        output: dict = json.loads(chunk)
                        yield output


async def httpx_async_chat(data: dict):
    stream = data["stream"]
    async with httpx.AsyncClient() as client:
        if not stream:
            response: httpx.Response = await client.post(URL, json=data)
            yield response.json()
        else:
            async with client.stream("POST", URL, json=data) as response:
                chunk: str
                async for chunk in response.aiter_lines():
                    if chunk:
                        output: dict = json.loads(chunk)
                        yield output


async def readex_async_chat(data: dict):
    async for output in httpx_async_chat(data):
        print(output)


if __name__ == "__main__":
    data = {
        "messages": [{"content": "讲一个猫和老鼠的故事", "role": "user"}],
        "max_new_tokens": 1024,
        "temperature": 0.8,
        "top_p": 0.8,
        "top_k": 50,
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

    asyncio.run(readex_async_chat(data))
    asyncio.run(readex_async_chat(data_stream))
