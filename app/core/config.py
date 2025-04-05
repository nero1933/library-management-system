
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    MAX_BORROWS: int
    DISABLE_SQL_LOGGING: bool

    # model_config = ConfigDict(env_file=".env")

    class Config:
        env_file = ".env"

settings = Settings()
