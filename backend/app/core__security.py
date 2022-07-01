from datetime import datetime, timedelta

from dataclasses import dataclass

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
from jose import JWTError, jwt

from schemas__tokens import TokenPayloadSchema

from core__config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class PasswordManager():
  password_context: CryptContext = password_context

  def verify_password(self, password: str, hashed_pass: str) -> bool:
    return self.password_context.verify(password, hashed_pass)


@dataclass
class TokenMaker():
  token_algorithm: str = "HS256"
  jwt_secret_key: str = settings.JWT_SECRET_KEY
  access_token_expiration: timedelta = timedelta(days=30)
  refresh_token_expiration: timedelta = timedelta(days=90)

  def _create_token(self, sub: str, expiration: timedelta) -> str:
    to_encode = {"exp": datetime.utcnow() + expiration, "sub": sub}
    return jwt.encode(to_encode, self.jwt_secret_key, algorithm=self.token_algorithm)

  def create_access_token(self, sub: str) -> str:
    return self._create_token(sub, self.access_token_expiration)

  def create_refresh_token(self, sub: str) -> str:
    return self._create_token(sub, self.refresh_token_expiration)


class JWTBearer(HTTPBearer):

  def __init__(self, auto_error: bool = True, algorithms: list[str] = ["HS256"]):
    super(JWTBearer, self).__init__(auto_error=auto_error)
    self.algorithms = algorithms
    self.jwt_secret_key = settings.JWT_SECRET_KEY

  async def __call__(self, request: Request) -> str:
    # retrieve credentials
    credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
    # check credentials
    if not credentials:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Credentials were not provided.")
    if not credentials.scheme == "Bearer":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Invalid authentication scheme.")
    # verify credetionals
    return self.verify_token(credentials.credentials)

  def verify_token(self, token: str) -> str:
    try:
      payload = jwt.decode(token, self.jwt_secret_key,
                           algorithms=self.algorithms)
      token_payload = TokenPayloadSchema(**payload)
    except JWTError:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Invalid token or expired token.")
    return token_payload.dict()["sub"]
