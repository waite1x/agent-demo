"""
项目根路径自动注入说明
======================
已在虚拟环境 site-packages 中放置：

    .venv/lib/python3.13/site-packages/agent-api.pth

内容为项目根目录的绝对路径，Python 解释器启动时会自动将其加入
sys.path，无需任何代码干预。

效果：
- FastAPI 运行时：正常工作，路径已在 sys.path。
- devui 直接加载子模块：同样工作，.pth 文件已在启动时生效。

所有 workflow.py / agent.py 使用纯绝对导入即可：
    from app.agent.xxx import ...
"""
