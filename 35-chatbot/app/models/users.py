from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import (
    Base,
    int_pk,
    uuid_type,
    required_unique_string,
    required_string,
    string,
    timestamp,
    timestamp_default_now,
    timestamp_update_now,
)
from .conversations import ConversationDB


class UserDB(Base):
    # 表名
    __tablename__ = "chatbot_users"

    id: Mapped[int_pk]
    username: Mapped[required_string]
    password: Mapped[required_string]
    email: Mapped[required_unique_string]
    phone: Mapped[string]
    status: Mapped[string]
    uuid: Mapped[uuid_type]
    last_login_at: Mapped[timestamp] = mapped_column(
        nullable=True, comment="最后登录时间"
    )
    created_at: Mapped[timestamp_default_now]
    updated_at: Mapped[timestamp_update_now]
    deleted_at: Mapped[timestamp]

    # 关联字段
    conversations: Mapped[list[ConversationDB]] = relationship(
        ConversationDB, back_populates="user"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', phone='{self.phone}', status='{self.status}', uuid='{self.uuid}', created_at='{self.created_at}', updated_at='{self.updated_at}', deleted_at='{self.deleted_at}', conversation_num={len(self.conversations)})>"
