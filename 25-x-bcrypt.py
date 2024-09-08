import bcrypt

# bcrypt 专门用于密码 hash 和验证


# 哈希密码
password = "secret".encode("utf-8")

hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)
# b'$2b$12$VQoTe7XFivUfmUCLSpv.recCY2UrseBxdWVW1dMz1RfxVPyL1SbJW'

hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)
# b'$2b$12$gavoasB2oW4rCTSPyOodfeQu0sEBv.hL4oIAutRuwgWKnQs.bYMti'

# 验证密码
correct = bcrypt.checkpw(password, hashed)
print(correct)
# True
