import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf8"), hashed_password.encode("utf8"))


def get_password_hash(password: str) -> str:
    # return pwd_context.hash(password)
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")
