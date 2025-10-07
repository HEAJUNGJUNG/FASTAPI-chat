from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.auth.models import User
from app.chat import models, schemas
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

# 메모리에 연결된 클라이언트 저장
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    # 1. 쿼리 파라미터에서 토큰 꺼내기
    token = websocket.query_params.get("token")
    if not token:   # 👈 여기가 함수 안에서 4칸 들여쓰기
        await websocket.close()
        return

    # 2. 토큰 검증
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            await websocket.close()
            return
    except JWTError:
        await websocket.close()
        return

    # 3. 연결 성공 → 채팅방 등록
    await manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # DB 저장
            chat_message = models.ChatMessage(
                room_id=room_id,
                username=username,
                message=data,
                timestamp=datetime.utcnow()
            )
            db.add(chat_message)
            db.commit()

            # 브로드캐스트
            await manager.broadcast(room_id, {
                "username": username,
                "message": data,
                "timestamp": str(chat_message.timestamp)
            })
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

@router.get("/messages/{room_id}", response_model=List[schemas.ChatMessageResponse])
def get_messages(room_id: str, db: Session = Depends(get_db)):
    return db.query(models.ChatMessage).filter(models.ChatMessage.room_id == room_id).order_by(models.ChatMessage.timestamp).all()
