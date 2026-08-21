from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.cores.security import hash_password, verify_password,BadRequestError


def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )

    hashed_pwd = hash_password(user_data.password)


    new_user = User(
        email=user_data.email,
        password_hash=hashed_pwd,     
        full_name=user_data.full_name, 
        role=user_data.role,
        is_active=user_data.is_active
)

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user

def authenticate_user(db: Session, user_data: UserLogin):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise BadRequestError("Email hoặc mật khẩu không chính xác")

    if not user.is_active:
        raise BadRequestError("Tài khoản của bạn đã bị vô hiệu hóa")
    return user