from pydantic.fields import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Admin settings
    ADMIN_EMAIL: str = Field(..., env="ADMIN_EMAIL")
    ADMIN_NAME: str = Field(..., env="ADMIN_NAME")
    ADMIN_PASSWORD: str = Field(..., env="ADMIN_PASSWORD")
    # SMTP settings
    SMTP_HOST: str = Field(..., env="SMTP_HOST")
    SMTP_PORT: int = Field(..., env="SMTP_PORT")
    SMTP_USER: str = Field(..., env="SMTP_USER")
    SMTP_PASSWORD: str = Field(..., env="SMTP_PASSWORD")

    # JWT settings
    JWT_ALGORITHM: str = Field(..., env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(..., env="JWT_REFRESH_TOKEN_EXPIRE_MINUTES")

    KEYS_DIR: str = Field(..., env="KEYS_DIR")
            
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        

settings = Settings() 