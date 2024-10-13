import datetime
from uuid import UUID as _UUID
from sqlalchemy import Integer, String, Text, JSON, UUID, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column
from typing import Annotated

from .database import database_type


int_pk = Annotated[int, mapped_column(primary_key=True, comment="主键")]
uuid_type = Annotated[
    _UUID,
    mapped_column(
        UUID,
        unique=True,
        nullable=False,
        server_default=func.gen_random_uuid(),
        comment="UUID主键",
    ),
]
string = Annotated[str, mapped_column(String(256), unique=False, nullable=True)]
text = Annotated[str, mapped_column(Text, nullable=True)]
required_string = Annotated[
    str, mapped_column(String(256), unique=False, nullable=False)
]
required_unique_string = Annotated[
    str, mapped_column(String(256), unique=True, nullable=False)
]
default_zero_int = Annotated[int, mapped_column(Integer, default=0, comment="默认值0")]
json_type = Annotated[
    list[dict],
    mapped_column(
        JSONB if database_type == "postgresql" else JSON,
        nullable=True,
        comment="JSON格式",
    ),
]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=True,
        comment="时间戳",
    ),
]
timestamp_default_now = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.now(), comment="创建时间"),
]
timestamp_update_now = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    ),
]
