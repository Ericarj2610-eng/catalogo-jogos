from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
engine = create_engine(settings.DATABASE_URL)

class Base(DeclarativeBase):
    pass

def get_session():
    with Session(engine) as session:
        yield session