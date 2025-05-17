from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    app_name: str = "Attendance Service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000


app_settings = AppConfig()
