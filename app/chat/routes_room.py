from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.chat.room import ChatRoom
from app.chat.schemas import ChatRoomCreate, ChatRoomSelect
import uuid

router = APIRouter(prefix="/rooms", tags=["ChatRoom"])

# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 방 생성 API
@router.post("/createRooms")
def create_room(room: ChatRoomCreate, db: Session = Depends(get_db)):
    """새로운 채팅방 생성"""
    try:
        # 방 객체 생성
        room = ChatRoom(name=room.name, room_id=str(uuid.uuid4())[:6])

        # DB 저장
        db.add(room)
        db.commit()
        db.refresh(room)  # 새로 생성된 row 갱신

        return {"room_id": room.room_id, "name": room.name, "created_at": room.created_at}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"방 생성 실패: {e}")


# ✅ 방 조회 API
@router.post("/selectRooms")
def create_room(room: ChatRoomSelect, db: Session = Depends(get_db)):
    """채팅방 단일 조회"""
    try:
        # ✅ DB 조회
        selected_room = db.query(ChatRoom).filter(ChatRoom.room_id == room.room_id).first()

        if not selected_room:
            raise HTTPException(status_code=404, detail="해당 방을 찾을 수 없습니다.")

        return selected_room  # ✅ 자동으로 ChatRoomResponse로 직렬화됨
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"방 조회 실패: {e}")