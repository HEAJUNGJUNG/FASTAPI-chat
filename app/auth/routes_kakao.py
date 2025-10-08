from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# 카카오 로그인
@router.get("/kakao/login")
def kakao_login(request: Request):
    # 요청 들어온 서버의 기본 URL (예: http://127.0.0.1:8000/)
    base_url = str(request.base_url).rstrip("/")
    redirect_uri = f"{base_url}/auth/kakao/callback"

    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"client_id={settings.KAKAO_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
    )
    return RedirectResponse(kakao_auth_url)

@router.get("/kakao/callback")
def kakao_callback(request: Request):
    return {"msg": "카카오 로그인 완료 (추후 처리 가능)"}
