from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.schemas import UserCreate
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def login_user(user: User):
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

def get_password_hash(password: str) -> str:
    print(">>> RAW PASSWORD:", password, "LEN:", len(password.encode("utf-8")))
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.hash(password)
