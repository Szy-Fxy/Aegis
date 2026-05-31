# Python 技术栈规范

## 环境管理

```bash
# 优先使用 Poetry
poetry new my-project          # 新项目
poetry add <package>           # 加依赖
poetry add -D <dev-package>    # 加开发依赖
poetry install                 # 安装全部依赖

# 备选：venv + pip
python -m venv .venv
# Windows 激活：.venv\Scripts\activate
# macOS/Linux 激活：source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt  # 锁定依赖
```

## 项目结构

```
project/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       ├── core.py              # 核心逻辑
│       ├── models.py            # 数据模型（Pydantic / dataclass）
│       ├── services.py          # 业务服务层
│       └── utils.py             # 工具函数
├── tests/
│   ├── conftest.py              # pytest fixtures
│   ├── test_core.py
│   └── test_models.py
├── scripts/                     # 一次性脚本 / CLI 入口
├── pyproject.toml               # 项目元数据 + 依赖 + 工具配置
├── .env.example                 # 环境变量模板
└── README.md
```

## 代码风格

- 遵循 PEP 8
- 用 `ruff` 统一处理格式化和 lint（不要再单独用 black / isort / flake8）
  ```bash
  ruff format          # 格式化
  ruff check --fix     # 自动修复 lint 问题
  ```
- 类型注解必须写（函数参数和返回值）
- 用 `from __future__ import annotations`（Python 3.10+ 可选）

```python
from __future__ import annotations

def calculate_damage(base: float, multiplier: float = 1.0) -> float:
    return base * multiplier
```

## 常用库速查

| 场景 | 优先使用 | 备注 |
|------|----------|------|
| HTTP 客户端 | `httpx`（异步）/ `requests`（同步） | 新项目统一用 httpx |
| HTTP 服务端 | `FastAPI` | 异步 + 自动 OpenAPI 文档 |
| 数据处理 | `pandas` | 表格数据首选 |
| 数值计算 | `numpy` | 数组/矩阵运算 |
| CLI 工具 | `typer` | 基于类型注解自动生成 CLI |
| 配置管理 | `pydantic-settings` | 环境变量 + 配置文件 |
| 数据校验/序列化 | `pydantic` v2 | 替代 dataclass 做运行时校验 |
| 测试 | `pytest` + `pytest-cov` | 主流选择 |
| 异步 | `asyncio` + `anyio` | 标准库优先 |
| 图像处理 | `Pillow` / `opencv-python` | 按需选择 |
| 数据库 ORM | `SQLAlchemy` 2.x | 异步支持好 |
| 数据库迁移 | `alembic` | SQLAlchemy 配套 |
| 任务队列 | `celery` / `arq` | 同步用 celery，异步用 arq |
| 日志 | `loguru` | 比标准库 logging 好用 |

## 测试

```bash
pytest -v                          # 运行所有测试
pytest -v -k "keyword"             # 按关键字筛选
pytest --cov=src --cov-report=html # 覆盖率报告
```

### pyproject.toml 最小配置

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.ruff.format]
quote-style = "double"
```

## 类型注解规范

```python
# ✅ 现代风格（Python 3.10+）
def process(items: list[str], config: dict[str, int] | None = None) -> bool: ...

# ❌ 旧风格
from typing import List, Dict, Optional
def process(items: List[str], config: Optional[Dict[str, int]] = None) -> bool: ...
```