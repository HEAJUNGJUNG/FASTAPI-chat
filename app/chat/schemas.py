from pydantic import BaseModel
from datetime import datetime

class ChatMessageResponse(BaseModel):
    id: int
    room_id: str
    username: str
    message: str
    timestamp: datetime

class ChatRoomCreate(BaseModel):
    name: str

class ChatRoomSelect(BaseModel):
    room_id: str

class ChatRoomResponse(BaseModel):
    room_id: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True