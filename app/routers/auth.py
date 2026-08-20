from fastapi import APIRouter, status, Depends,Form

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


