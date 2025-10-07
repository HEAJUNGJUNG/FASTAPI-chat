import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI Productivity Hub"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"

settings = Settings()
