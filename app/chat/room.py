from sqlalchemy import Column, String, DateTime, func
from app.core.database import Base
import uuid

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    room_id = Column(String(8), primary_key=True, default=lambda: str(uuid.uuid4())[:6])
    name = Column(String(50))
    created_at = Column(DateTime, default=func.now())
