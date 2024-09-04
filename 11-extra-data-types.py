# https://fastapi.tiangolo.com/zh/tutorial/extra-data-types/
import uvicorn
from fastapi import FastAPI, Body
from datetime import datetime, time, timedelta
from uuid import UUID


app = FastAPI()


# 到目前为止，您一直在使用常见的数据类型，如:
#     int
#     float
#     str
#     bool
# 但是您也可以使用更复杂的数据类型。

# 您仍然会拥有现在已经看到的相同的特性:
#     很棒的编辑器支持。
#     传入请求的数据转换。
#     响应数据转换。
#     数据验证。
#     自动补全和文档。

# 其他数据类型
# 下面是一些你可以使用的其他数据类型:
#   - UUID:
#       - 一种标准的 "通用唯一标识符" ，在许多数据库和系统中用作ID。
#       - 在请求和响应中将以 str 表示。
#   - datetime.datetime:
#       - 一个 Python datetime.datetime.
#       - 在请求和响应中将表示为 ISO 8601 格式的 str ，比如: 2023-06-30T07:07:47.369Z
#   - datetime.date:
#       - Python datetime.date.
#       - 在请求和响应中将表示为 ISO 8601 格式的 str ，比如: 14:23:55.003
#   - datetime.timedelta:
#       - 一个 Python datetime.timedelta.
#       - 在请求和响应中将表示为 float 代表总秒数。
#       - Pydantic 也允许将其表示为 "ISO 8601 时间差异编码", 查看文档了解更多信息。
#   - frozenset:
#       - 在请求和响应中，作为 set 对待：
#           - 在请求中，列表将被读取，消除重复，并将其转换为一个 set。
#           - 在响应中 set 将被转换为 list 。
#           - 产生的模式将指定那些 set 的值是唯一的 (使用 JSON 模式的 uniqueItems)。
#   - bytes:
#       - 标准的 Python bytes。
#       - 在请求和相应中被当作 str 处理。
#       - 生成的模式将指定这个 str 是 binary "格式"。
#   - Decimal:
#       - 标准的 Python Decimal。
#       - 在请求和相应中被当做 float 一样处理。
# http://127.0.0.1:8000/docs
@app.post("/items/{item_id}")
async def read_items(
    item_id: UUID,                                          # ex: 6F9619FF-8B86-D011-B42D-00C04FC964FF
    start_datetime: datetime | None = Body(default=None),   # ex: 2023-06-30T07:07:47.369Z
    end_datetime: datetime | None = Body(default=None),     # ex: 2023-06-30T07:07:47.369Z
    repeat_at: time | None = Body(default=None),            # ex: 07:10:58.704
    process_after: timedelta | None = Body(default=None),   # ex: 1534
):
    # 注意，函数内的参数有原生的数据类型，你可以，例如，执行正常的日期操作，如:
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


# run: uvicorn main:app --reload --port=8000
#   main: main.py 文件(一个 Python「模块」)。
#   app: 在 main.py 文件中通过 app = FastAPI() 创建的对象。
#   --reload: 让服务器在更新代码后重新启动。仅在开发时使用该选项。
if __name__ == "__main__":
    import os
    from pathlib import Path

    # 从环境变量中获取端口号，默认为 8000
    port = int(os.getenv('PORT', 8000))

    # 从环境变量中获取主机地址，默认为 0.0.0.0
    host = os.getenv('HOST', '0.0.0.0')

    file = Path(__file__).stem  # get file name without suffix
    # 不使用 reload = True 时可以直接传递 app 对象
    uvicorn.run(app=f"{file}:app", host=host, port=port, reload=True)
