import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

from app.core.config import settings


def generate_code() -> str:
    """6자리 인증코드 생성"""
    return str(randint(100000, 999999))

def send_verification_email(to_email: str, code: str):
    """수신자에게 인증코드 메일 발송"""
    subject = "FASTAPI CHAT 이메일 인증코드"
    body = f"""
    안녕하세요 👋  
    아래의 인증코드를 입력해주세요.

    ✅ 인증코드: {code}

    (5분 이내에 입력해야 합니다.)
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_SENDER
    msg["To"] = to_email

    try:
        # ✅ TLS 방식 사용 (port=587)  / 465 포트는 SSL방식 with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as smtp:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as smtp:
            smtp.starttls()  # ✅ 반드시 있어야 함
            smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
            smtp.send_message(msg)

        print(f"[메일 전송 성공] {to_email}")
    except Exception as e:
        print(f"[메일 전송 실패] {e}")
