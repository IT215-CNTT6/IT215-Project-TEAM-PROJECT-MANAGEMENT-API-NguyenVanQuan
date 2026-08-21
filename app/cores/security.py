from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.cores.config import settings

# Lớp lỗi cha
class AppException(Exception):
    status_code = 500
    message = "Lỗi hệ thống"

    def __init__(self, message: str = None):
        # Nếu truyền thông báo mới thì đè lên thông báo mặc định
        if message:
            self.message = message

# 3 Lỗi chính (Đã cài sẵn thông báo mặc định)
class BadRequestError(AppException):
    status_code = 400
    message = "Dữ liệu gửi lên không hợp lệ"

class ForbiddenError(AppException):
    status_code = 403
    message = "Bạn không có quyền truy cập"

class NotFoundError(AppException):
    status_code = 404
    message = "Không tìm thấy dữ liệu"

# Hàm bắt lỗi tập trung
def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "code": exc.status_code,
                "message": exc.message
            }
        )



def hash_password(password: str, cost_factor: int = 12) -> str:
    """
    Băm mật khẩu sử dụng thư viện bcrypt trực tiếp.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập vào có khớp với mật khẩu đã băm trong DB hay không.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    """
    Tạo Access Token (JWT) dựa trên thông tin payload (data) được truyền vào.
    """
    to_encode = data.copy()

    # Tính toán thời gian hết hạn (expiration time) - đọc từ config
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Ký và tạo chuỗi token bằng thư viện PyJWT - đọc SECRET_KEY từ config
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt