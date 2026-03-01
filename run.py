"""
开发启动脚本
运行方式：
  python run.py          # 直接运行（热重载）
  uvicorn run:app        # uvicorn 直接引用
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
