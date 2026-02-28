# ---- build stage ----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt \
    # 预编译字节码，加速首次启动
    && python -m compileall /install/lib -q \
    # 删除测试目录、dist-info 中的 RECORD 等无用文件
    && find /install -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true \
    && find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /install -name "*.dist-info" -exec rm -rf {}/RECORD {} + 2>/dev/null || true

# ---- runtime stage ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 仅复制运行所需的已安装包
COPY --from=builder /install /usr/local

# 删除 apt 缓存 & pip & wheel（运行时不需要）
RUN apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* /root/.cache \
    && pip uninstall -y pip setuptools wheel 2>/dev/null || true

# 复制应用代码（排除 .dockerignore 中的条目）
COPY app/ ./app/
COPY run.py .

# 创建日志目录并设置非 root 用户
RUN mkdir -p logs \
    && addgroup --system appgroup \
    && adduser --system --ingroup appgroup --no-create-home appuser \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
