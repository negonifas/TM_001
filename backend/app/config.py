from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    auth_secret: str
    cookie_secure: bool = False
    cookie_max_age_days: int = 30

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
