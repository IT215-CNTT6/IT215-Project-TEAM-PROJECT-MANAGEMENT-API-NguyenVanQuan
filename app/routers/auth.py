from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session

# Import Database Session
from app.db.database import get_db

# Import Schemas
from app.schemas.user import UserCreate, UserLogin, UserResponse

# Import Service (Lưu ý đặt đúng tên import service_user)
from app.services import service_user

# Import Security Helpers
from app.cores.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/form", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    email: str = Form(..., description="Email của người dùng"),
    password: str = Form(..., description="Mật khẩu"),
    full_name: str = Form(..., description="Họ và tên người dùng"),  
    role: str = Form("USER", description="Vai trò (USER / ADMIN)"),    
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản bằng Form-Data.
    """
    # Khởi tạo Pydantic Schema từ dữ liệu Form
    user_data = UserCreate(
        email=email, 
        password=password, 
        full_name=full_name, 
        role=role
    )
    
    # Sửa từ servie_user -> service_user
    new_user = service_user.create_user(db=db, user_data=user_data)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint Đăng nhập bằng JSON request (email, password).
    """
    # Sửa từ servie_user -> service_user
    user = service_user.authenticate_user(db=db, user_data=user_data)

    # Lấy role trực tiếp từ user model
    role_name = user.role

    # Tạo JWT Access Token
    access_token = create_access_token(
        data={
            "sub": user.email, 
            "id": user.id, 
            "role": role_name
        }
    )

    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }