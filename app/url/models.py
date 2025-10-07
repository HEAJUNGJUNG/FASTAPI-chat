from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(1000), nullable=False)
    short_code = Column(String(20), unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class URLClickLog(Base):
    __tablename__ = "url_click_logs"

    id = Column(Integer, primary_key=True, index=True)
    short_url_id = Column(Integer, ForeignKey("short_urls.id", ondelete="CASCADE"))
    ip_address = Column(String(100))
    user_agent = Column(String(300))
    clicked_at = Column(DateTime, default=datetime.utcnow)
