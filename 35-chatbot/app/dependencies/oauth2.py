from fastapi.security import OAuth2PasswordBearer


# 创建 OAuth2 密码端点。
# 该端点用于获取 JWT 访问令牌。
# 该端点需要用户名和密码，并返回 JWT 访问令牌。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
