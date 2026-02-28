"""
日志系统
- 同时输出到控制台（彩色）和滚动文件
- 基于标准库 logging + RotatingFileHandler
"""
import logging
import logging.handlers
import os
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """控制台彩色日志格式器"""

    COLORS = {
        "DEBUG":    "\033[36m",   # cyan
        "INFO":     "\033[32m",   # green
        "WARNING":  "\033[33m",   # yellow
        "ERROR":    "\033[31m",   # red
        "CRITICAL": "\033[35m",   # magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setup_logging(
    log_level: Optional[str] = None,
    log_dir: Optional[str] = None,
    log_filename: Optional[str] = None,
    log_format: Optional[str] = None,
    max_bytes: Optional[int] = None,
    backup_count: Optional[int] = None,
) -> None:
    """
    初始化日志系统。
    参数均有默认值，会从 settings 中读取，也可在测试时手动覆盖。
    """
    # 延迟导入，避免循环依赖
    from app.config import settings

    _level       = log_level    or settings.LOG_LEVEL
    _dir         = log_dir      or settings.LOG_DIR
    _filename    = log_filename or settings.LOG_FILENAME
    _fmt         = log_format   or settings.LOG_FORMAT
    _max_bytes   = max_bytes    or settings.LOG_MAX_BYTES
    _backup      = backup_count or settings.LOG_BACKUP_COUNT

    numeric_level = getattr(logging, _level.upper(), logging.INFO)

    # 确保日志目录存在
    os.makedirs(_dir, exist_ok=True)
    log_file_path = os.path.join(_dir, _filename)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # 避免重复添加 handler
    if root_logger.handlers:
        root_logger.handlers.clear()

    plain_formatter  = logging.Formatter(_fmt)
    color_formatter  = ColoredFormatter(_fmt)

    # ---- 控制台 handler ----
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(color_formatter)
    root_logger.addHandler(console_handler)

    # ---- 文件 handler（滚动） ----
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=_max_bytes,
        backupCount=_backup,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(plain_formatter)
    root_logger.addHandler(file_handler)

    # 抑制第三方库过多日志
    for noisy in ("uvicorn.access", "httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        f"日志系统已初始化 | 级别={_level} | 文件={log_file_path}"
    )
