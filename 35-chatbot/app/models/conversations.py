from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import (
    Base,
    int_pk,
    string,
    default_zero_int,
    json_type,
    timestamp,
    timestamp_default_now,
    timestamp_update_now,
)
from typing import TYPE_CHECKING  # for type hinting, 可以解决循环导入问题

if TYPE_CHECKING:
    from .users import UserDB
    from .models import ModelDB


class ConversationDB(Base):
    __tablename__ = "chatbot_conversations"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("chatbot_users.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("chatbot_models.id"))
    messages: Mapped[json_type]
    input_tokens: Mapped[default_zero_int]
    output_tokens: Mapped[default_zero_int]
    status: Mapped[string]
    created_at: Mapped[timestamp_default_now]
    updated_at: Mapped[timestamp_update_now]
    deleted_at: Mapped[timestamp]

    # 关联字段
    user: Mapped["UserDB"] = relationship("UserDB", back_populates="conversations")
    model: Mapped["ModelDB"] = relationship("ModelDB", back_populates="conversations")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, model_id={self.model_id}, messages={self.messages}, input_tokens_sum={self.input_tokens_sum}, output_tokens_sum={self.output_tokens_sum}, status='{self.status}')>"
