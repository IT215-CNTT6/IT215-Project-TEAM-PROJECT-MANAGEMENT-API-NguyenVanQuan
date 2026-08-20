from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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