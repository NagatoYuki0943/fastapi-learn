from .core import engine, Session, Base  # Noqa
from .models import ConversationDB, ModelDB, UserDB  # Noqa


# Create all tables
Base.metadata.create_all(engine)
