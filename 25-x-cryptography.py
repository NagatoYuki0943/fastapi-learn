from cryptography.fernet import Fernet
from datetime import datetime


# Fernet 提供了对称加密功能，可以用于加密和解密数据，但它的设计主要是为了保护数据的机密性，而不是专门用于密码存储和验证。
# 如果使用 Fernet 加密密码，密钥必须安全地存储。如果密钥泄露，攻击者可以解密所有存储的密码。
# 而使用哈希存储时，即使数据库被攻破，攻击者也无法轻易获取原始密码。


key = Fernet.generate_key()
print(key)
# b'YUk-F7fTUU776di8QOJeSZuzf4JhitGTNizmGNKdUjI='

fernet = Fernet(key)

secret = "my_secret"
secret_encoded = secret.encode('utf-8')
print(secret_encoded)
# b'my_secret'

encrypted = fernet.encrypt(secret_encoded)
print(encrypted)
# b'gAAAAABm3YjYs1dg1HIfZ7DVAw7MFsfg6ZeOjQfhUa2LEk2ZMYdFTWv585J-D4LGfZXb6nA8VijGHEhrSaUi-w0ys5jR7j3i2A=='

decrypted = fernet.decrypt(encrypted)
print(decrypted)
# b'my_secret'

# 每次加密后，密钥都会变化，所以无法直接解密
encrypted = fernet.encrypt(secret_encoded).decode('utf-8')
print(encrypted)
# gAAAAABm3YjY3BiwoUEiMDalYC3lbdz2U-tRPruzAIkfTLqv70OUvPnIbV846O6249rrPKEYHnarWzxDqkdfqPKU03EXnadbDA==

decrypted = fernet.decrypt(encrypted)
print(decrypted)
# b'my_secret'

timestamp = fernet.extract_timestamp(encrypted)
print(timestamp)
# 1725794520

datetime_obj: datetime = datetime.fromtimestamp(timestamp)
print(datetime_obj)
# 2024-09-08 19:22:00
