from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.mailer import send_verification_email, generate_code
from app.auth.service_email import save_verification_code, verify_code

router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ 요청 Body 명시
class EmailRequest(BaseModel):
    email: str


class VerifyRequest(BaseModel):
    email: str
    code: str

@router.post("/send-email")
def send_email(req: EmailRequest):
    email = req.email.strip()
    if not email:
        raise HTTPException(status_code=400, detail="이메일을 입력해주세요")

    code = generate_code()
    save_verification_code(email, code)
    send_verification_email(email, code)
    return {"message": "인증코드가 전송되었습니다"}

@router.post("/verify-email")
def verify_email(req: VerifyRequest):
    email = req.email.strip()
    code = req.code.strip()

    if not email or not code:
        raise HTTPException(status_code=400, detail="이메일과 코드를 입력해주세요")

    if verify_code(email, code):
        return {"message": "이메일 인증 성공!"}
    else:
        raise HTTPException(status_code=401, detail="인증 실패 또는 코드 만료")
