"""
应用配置管理（基于 pydantic-settings，支持 .env 文件）
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """应用全局配置"""

    # ------- 基本信息 -------
    APP_NAME: str = "Agent API Service"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "基于 FastAPI 的 Agent API 服务"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development / testing / production

    # ------- API 前缀 -------
    API_V1_PREFIX: str = "/api/v1"

    # ------- 服务器 -------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ------- 日志 -------
    LOG_LEVEL: str = "INFO"           # DEBUG / INFO / WARNING / ERROR / CRITICAL
    LOG_DIR: str = "logs"
    LOG_FILENAME: str = "app.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024   # 10 MB
    LOG_BACKUP_COUNT: int = 5
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"

    # ------- CORS -------
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # ------- 安全 / JWT（预留） -------
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ------- 数据库（预留） -------
    DATABASE_URL: Optional[str] = None

    # ------- Redis（预留） -------
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
