from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.auth.models import User
from app.url import models, schemas, utils
from typing import List

router = APIRouter(prefix="/url", tags=["URL Shortener"])

@router.post("/", response_model=schemas.URLResponse)
def create_short_url(
    url: schemas.URLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # short_code 생성 (중복 방지)
    short_code = utils.generate_short_code()
    while db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first():
        short_code = utils.generate_short_code()

    new_url = models.ShortURL(
        original_url=url.original_url,
        short_code=short_code,
        user_id=current_user.id
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@router.get("/{short_code}")
def redirect_short_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    url = db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    # 클릭 수 증가
    url.clicks += 1
    db.commit()

    # 클릭 로그 기록
    log = models.URLClickLog(
        short_url_id=url.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", "unknown")
    )
    db.add(log)
    db.commit()

    return RedirectResponse(url.original_url)

@router.get("/stats/{short_code}", response_model=schemas.URLResponse)
def get_url_stats(short_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url = db.query(models.ShortURL).filter(
        models.ShortURL.short_code == short_code,
        models.ShortURL.user_id == current_user.id
    ).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

@router.get("/stats/{short_code}/logs", response_model=List[schemas.URLClickLogResponse])
def get_click_logs(short_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url = db.query(models.ShortURL).filter(
        models.ShortURL.short_code == short_code,
        models.ShortURL.user_id == current_user.id
    ).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    logs = db.query(models.URLClickLog).filter(models.URLClickLog.short_url_id == url.id).all()
    return logs
