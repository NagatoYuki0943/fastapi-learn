from passlib.context import CryptContext    # pip install passlib bcrypt==4.0.1
# passlib 2020年停止更新, 因此直接使用 bcrytp 库代替


# passlib 对于同一个字符串每次生成的哈希值都不同。
# PassLib 对于同一个字符串每次生成不同的哈希值主要是通过使用"盐"(salt)来实现的。
# 盐是一个随机生成的字符串，每次哈希时都会生成一个新的盐。
#   - 当你使用 PassLib 对密码进行哈希时，它会自动生成一个随机盐。
#   - 将这个盐与原始密码组合。
#   - 对组合后的字符串进行哈希运算。
#   - 最终的哈希值通常包含盐和哈希结果。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


password = "password123"
hashed_password1 = pwd_context.hash(password)
print(hashed_password1)
# $2b$12$myNVyZbB4oWv8QRopnCh.enNGCoMX9Htv/RlDTsMy3L3uMN.lKnge

correct = pwd_context.verify(password, hashed_password1)
print(correct)
# True

hashed_password2 = pwd_context.hash(password)
print(hashed_password2)
# $2b$12$9iNoRQhhvJ6o8LQtk6uT8u/LfzhrbL97W8450Ggt4UIaN0mLIBU4u

correct = pwd_context.verify(password, hashed_password1)
print(correct)
# True
