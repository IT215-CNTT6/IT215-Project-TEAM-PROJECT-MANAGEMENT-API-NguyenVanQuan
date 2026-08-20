from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import project,projectMember,user,task
from app.routers import auth
from app.cores.security import setup_exception_handlers


app = FastAPI(
    title="TEAM PROJECT MANAGEMENT API"
)

Base.metadata.create_all(bind = engine)
setup_exception_handlers(app)
app.include_router(auth.router)

@app.get("/")
def get_root():
    return { "message": "Server đang khởi chạy" }

