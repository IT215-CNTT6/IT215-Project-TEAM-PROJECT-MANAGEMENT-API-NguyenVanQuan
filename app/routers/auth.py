from fastapi import APIRouter, status, Depends

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)