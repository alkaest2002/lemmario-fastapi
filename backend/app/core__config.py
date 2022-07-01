from pydantic import BaseSettings


class Settings(BaseSettings):
  JWT_SECRET_KEY: str
  ADMIN_EMAIL: str
  ADMIN_PASS: str
  ADMIN_HASHED_PASS: str
  DATABASE_URL: str

  class Config:
    case_sensitive = True
    env_file = ".env"


settings = Settings()
