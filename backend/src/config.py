from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:////app/backend/sql_app.db"
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    VERIFIED_JOB_BOARDS: list[str] = ["LinkedIn", "Indeed", "Dice"]

    class Config:
        env_file = ".env"


settings = (
    Settings()
)  # Keep this line for backward compatibility if other files are already importing and using 'settings' directly
