# Contributing

## 运行测试

```bash
# 全部测试
pytest tests/ -q

# 单个模块
pytest tests/test_state_manager.py -q

# 含覆盖率（需要 pytest-cov）
pytest tests/ -q --cov=src/aegis_toolchain --cov-report=term-missing
```

## 代码检查

```bash
ruff check src/ tests/
mypy src/ tests/
```

## 安装开发依赖

```bash
pip install -e .[dev]
```

## 写新测试

- 测试文件命名：`tests/test_<模块名>.py`
- 测试辅助函数从 `helpers` 导入：`from helpers import make_req, make_state`
- 使用 `temp_project` / `clean_project` fixture 获取隔离的临时目录
