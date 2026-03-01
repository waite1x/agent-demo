"""
项目根路径自动注入说明
======================
通过 pyproject.toml 可编辑安装来解决，无需任何代码干预：

    pip install -e .

pip 会在虚拟环境 site-packages 中自动生成：

    __editable__.agent_api-1.0.0.pth  ← 指向项目根目录

效果：
- FastAPI 运行时：app.* 绝对导入正常。
- devui 直接加载子模块：同样正常，.pth 在解释器启动时已生效。
- 新机器/CI 环境搭建：pip install -r requirements.txt && pip install -e . 即可。

所有 workflow.py / agent.py 使用纯绝对导入，无需任何 sys.path 操作：
    from app.agent.xxx import ...
"""
