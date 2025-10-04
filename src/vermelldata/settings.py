from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    purpleair_key: str
    db_url: str = "duckdb:///data/vermelldata.duckdb"

    class Config:
        env_file = ".env"


settings = Settings()  # import anywhere: from vermelldata.settings import settings

