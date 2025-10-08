from datetime import datetime, timedelta

# 임시 저장소 (Redis를 안 쓸 경우)
TEMP_CODES = {}

def save_verification_code(email: str, code: str):
    """이메일별 인증코드 저장 (유효시간 5분)"""
    TEMP_CODES[email] = {
        "code": code,
        "expires_at": datetime.utcnow() + timedelta(minutes=5)
    }

def verify_code(email: str, code: str) -> bool:
    """인증코드 확인"""
    entry = TEMP_CODES.get(email)
    if not entry:
        return False

    if datetime.utcnow() > entry["expires_at"]:
        del TEMP_CODES[email]
        return False

    if entry["code"] == code:
        del TEMP_CODES[email]
        return True

    return False
