import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI Productivity Hub"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # Brevo SMTP 설정
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASS: str = os.getenv("SMTP_PASS")
    MAIL_SENDER: str = os.getenv("MAIL_SENDER")

    # Kakao Login
    KAKAO_CLIENT_ID: str = os.getenv("KAKAO_CLIENT_ID")

settings = Settings()
