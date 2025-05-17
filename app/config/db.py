from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@attendance-db:5432/attendance_db"


db_settings = DatabaseConfig()
