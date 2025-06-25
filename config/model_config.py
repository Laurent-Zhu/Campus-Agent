from pydantic_settings import BaseSettings
from typing import List

class ModelConfig(BaseSettings):
    """模型配置"""
    API_KEY: str
    API_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v3"
    API_VERSION: str = "chatglm_turbo"

    class Config:
        env_file = ".env"
        extra = "allow"  # 允许额外的环境变量