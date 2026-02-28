"""
开发启动脚本
运行方式：python run.py
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,          # 开发时热重载
        log_level=settings.LOG_LEVEL.lower(),
    )
