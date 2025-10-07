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
    # 1️⃣ 토큰 검증
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close()
        return

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            await websocket.close()
            return
    except JWTError:
        await websocket.close()
        return

    # 2️⃣ 연결 등록
    await manager.connect(room_id, websocket)

    try:
        while True:
            # 프론트엔드에서 {"username": "익명", "message": "내용"} 으로 보낸다고 가정
            data = await websocket.receive_json()
            
            # 혹시라도 message가 dict로 들어온 경우 방어 코드
            if isinstance(data.get("message"), dict):
                message_text = data["message"].get("message", "")
                sender = data["message"].get("username", username)
            else:
                message_text = data.get("message", "")
                sender = data.get("username", username)

            # DB 저장
            chat_message = models.ChatMessage(
                room_id=room_id,
                username=sender,
                message=message_text,  # ✅ 문자열만 들어가도록 보장
                timestamp=datetime.utcnow()
            )
            db.add(chat_message)
            db.commit()

            # broadcast
            await manager.broadcast(room_id, {
                "username": sender,
                "message": message_text,
                "timestamp": chat_message.timestamp.strftime("%H:%M:%S")
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, {
            "username": "SYSTEM",
            "message": f"{username} 님이 퇴장했습니다.",
            "timestamp": datetime.utcnow().strftime("%H:%M:%S")
        })


@router.get("/messages/{room_id}", response_model=List[schemas.ChatMessageResponse])
def get_messages(room_id: str, db: Session = Depends(get_db)):
    """이전 채팅 내역 조회"""
    return db.query(models.ChatMessage).filter(models.ChatMessage.room_id == room_id).order_by(models.ChatMessage.timestamp).all()
