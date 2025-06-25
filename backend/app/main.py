from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# from app.api.endpoints import exam, auth
# from app.db.session import engine
# from app.models.base import Base
from backend.app.core.config import settings
from backend.app.api.endpoints import exam, auth
from backend.app.db.session import engine
from backend.app.models.base import Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # 必须包含"Authorization"
)

# 注册 /api/v1/exams 路由
app.include_router(
    exam.router,
    prefix=f"{settings.API_V1_STR}/exams",
    tags=["exam"]
)
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

# 启动时自动建表（仅开发环境用，生产建议用alembic）
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Campus Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}