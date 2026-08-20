from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.cores.security import hash_password, verify_password,BadRequestError


def create_user(db: Session, user_data: UserCreate):
    """
    Logic Đăng ký tài khoản:
    1. Kiểm tra xem email đã tồn tại trong database chưa.
    2. Nếu tồn tại, ném ra lỗi HTTPException (400 Bad Request).
    3. Tìm kiếm role theo tên (role_name) trong bảng roles.
    4. Băm mật khẩu người dùng.
    5. Lưu thông tin người dùng (với role_id và mật khẩu đã băm) vào database.
    """
    # 1. Kiểm tra email tồn tại
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )


    # 3. Băm mật khẩu bằng helper
    hashed_pwd = hash_password(user_data.password)

    # 4. Tạo User model instance mới, gán role_id (khóa ngoại) thay vì chuỗi role
    new_user = User(
        email=user_data.email,
        password_hash=hashed_pwd,     
        full_name=user_data.full_name, 
        role=user_data.role,
        is_active=user_data.is_active
)

    # 5. Thêm vào session và lưu xuống DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Cập nhật lại new_user với thông tin lấy từ DB

    return new_user

def authenticate_user(db: Session, user_data: UserLogin):
    """
    Logic Đăng nhập:
    1. Tìm người dùng trong database theo email.
    2. Nếu không tìm thấy, hoặc nếu có mà mật khẩu không khớp -> lỗi 400.
    3. Trả về thông tin người dùng nếu thành công.
    """
    # 1. Tìm user theo email
    user = db.query(User).filter(User.email == user_data.email).first()

    # 2. Kiểm tra user có tồn tại không VÀ mật khẩu có khớp không
    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # 3. Đăng nhập thành công, trả về model user
    return user