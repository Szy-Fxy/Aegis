# Aegis Toolchain 使用指南

---

## 🌱 我不会命令行

**Windows**：下载 [install.ps1](https://github.com/Szy-Fxy/Aegis/raw/main/install.ps1)，右键 → "使用 PowerShell 运行"，几秒钟完事。

**Mac**：打开终端，粘贴：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.sh)"
```

装好后，打开终端：

```bash
cd 你的项目目录
aegis start "我的第一个需求"
```

——你已经创建了第一个需求。

### 接下来

| 我想... | 输入 |
|---------|------|
| 看所有需求 | `aegis status` |
| 标记需求完成 | `aegis devlog write REQ-001 -m "做完了"` 然后 `aegis advance` |
| 查看更多命令 | `aegis --help` |

---

## 🧠 我会命令行

```bash
pip install git+https://github.com/Szy-Fxy/Aegis.git
cd 我的项目
aegis start "测试" --level auto
aegis status
```

---

## 🛠 我是开发者，想要源码

```bash
git clone https://github.com/Szy-Fxy/Aegis.git
cd Aegis
pip install -e .
```

---

## 📖 完整命令

| 命令 | 干什么 | 举例 |
|------|--------|------|
| `aegis start "标题"` | 开始一个需求 | `aegis start "修登录bug"` |
| `aegis start "标题" -l L2` | 开始需求（指定等级） | `aegis start "炮台系统" -l L2` |
| `aegis start "标题" --level auto` | 让系统自动判断等级 | |
| `aegis status` | 看所有需求进度 | |
| `aegis status REQ-001` | 看某个需求详情 | |
| `aegis status --json` | JSON 格式输出 | |
| `aegis check` | 检查当前阶段是否通过 | |
| `aegis check REQ-001` | 检查指定需求 | |
| `aegis advance` | 推进到下一阶段 | |
| `aegis advance -f` | 强制推进（跳过检查） | |
| `aegis devlog write REQ-001 -m "内容"` | 写开发日志 | |
| `aegis devlog show` | 看最近的日志 | |
| `aegis preprocess "消息"` | 预处理用户消息 | |

### 需求等级

| 等级 | 什么时候用 | 流程 |
|------|-----------|------|
| L1 | 修 bug、改配置、typo | 登记 → 改代码 → DevLog → 完成 |
| L2 | 加功能、优化 | 设计 → 实现 → DevLog → 完成 |
| L3 | 架构重构 | 7 阶段全流程 |
| auto | 不确定 | 系统自动判断 |

---

## 🔧 L2 需求完整示范

```bash
# 1. 开始
aegis start "捕鱼炮台系统" -l L2

# 2. 创建设计文档
#    在 Aegis_Specs/L2/捕鱼炮台系统/design.md 写内容

# 3. 检查
aegis check          # 显示 3/3 通过

# 4. 推进
aegis advance        # design → 🔨 implementing

# 5. 写代码...

# 6. 写日志
aegis devlog write REQ-001 -m "实现了炮台瞄准"

# 7. 完成
aegis advance        # 🎉 已完成
```

---

## 🔒 Git 提交时自动检查

在项目目录创建 `.pre-commit-config.yaml`：

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

```bash
pip install pre-commit
pre-commit install
```

之后每次 `git commit` 自动检查。

---

## 🆘 出问题了

| 症状 | 试试 |
|------|------|
| `aegis` 命令不存在 | 重启终端，或重新 `pip install git+...` |
| state.json 报错 | 删 `Aegis/state/state.json`，重新 `aegis start` |
| 一直卡住 | 关掉其他终端窗口 |
| 中文乱码（PowerShell） | 输入 `chcp 65001` |
