from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.api import exam

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Campus Agent API",
    description="教学实训智能体系统API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=eval(os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    exam.router,
    prefix="/api",
    tags=["exam"]
)