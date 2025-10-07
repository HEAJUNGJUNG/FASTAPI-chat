from pydantic import BaseModel
from datetime import datetime

class ChatMessageResponse(BaseModel):
    id: int
    room_id: str
    username: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True
