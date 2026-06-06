# Aegis Toolchain 使用指南

---

## 安装

```bash
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

然后：

```bash
cd 我的项目
aegis start "第一个需求"
aegis status
```

> 开发者取源码：`git clone https://github.com/Szy-Fxy/Aegis.git && cd Aegis && pip install -e .`

---

## 快速上手

| 我想... | 输入 |
|---------|------|
| 开始需求 | `aegis start "修登录bug"` |
| 开始需求（指定等级） | `aegis start "炮台系统" -l L2` |
| 让系统判断等级 | `aegis start "标题" --level auto` |
| 看所有需求 | `aegis status` |
| 看某个需求详情 | `aegis status REQ-001` |
| JSON 输出 | `aegis status --json` |
| 检查当前阶段 | `aegis check` |
| 推进到下一步 | `aegis advance` |
| 强制推进 | `aegis advance -f` |
| 写开发日志 | `aegis devlog write REQ-001 -m "内容"` |
| 看日志 | `aegis devlog show` |
| 完成需求 | `aegis devlog write REQ-001 -m "做完了"` 然后 `aegis advance` |

## 需求等级

| 等级 | 什么时候用 | 流程 |
|------|-----------|------|
| L1 | 修 bug、改配置 | 登记 → 改代码 → DevLog → 完成 |
| L2 | 加功能、优化 | 设计 → 实现 → DevLog → 完成 |
| L3 | 架构重构 | 7 阶段全流程 |
| auto | 不确定 | 系统自动判断 |

## L2 完整示范

```bash
aegis start "捕鱼炮台系统" -l L2
# 在 Aegis_Specs/L2/捕鱼炮台系统/design.md 写设计内容
aegis check        # 3/3 通过
aegis advance      # design → implementing
# 写代码...
aegis devlog write REQ-001 -m "实现了炮台瞄准"
aegis advance      # 🎉 完成
```

## Git 提交时自动检查

```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml`：

```yaml
repos:
  - repo: local
    hooks:
      - id: aegis
        name: Aegis Check
        entry: python -m aegis_toolchain.hooks.pre_commit
        language: system
        pass_filenames: false
        always_run: true
```

## 出问题了

| 症状 | 试试 |
|------|------|
| `aegis` 命令不存在 | 重启终端 |
| state.json 报错 | 删 `Aegis/state/state.json` |
| 中文乱码（PowerShell） | `chcp 65001` |
