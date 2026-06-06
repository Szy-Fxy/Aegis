# Aegis Toolchain 使用指南

---

## 🌱 小白 30 秒上手

### 我不会命令行，怎么装？

**Windows 用户**：下载 `install.ps1`，右键 → "使用 PowerShell 运行"，一路回车。

**Mac 用户**：打开终端，粘贴下面两行：

```bash
curl -O https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.sh
bash install.sh
```

装完后，打开终端（或 PowerShell），输入：

```bash
aegis start "我的第一个需求"
```

完了。你已经创建了第一个需求。

### 我想看现在有什么需求

```bash
aegis status
```

就这一条命令，所有的需求、状态、进度全显示出来。

### 我做完了一个需求，怎么标记完成

```bash
aegis devlog write REQ-001 -m "修好了登录按钮颜色"
aegis advance
```

两行完事。

---

## 🔧 极客完整教程

> 💡 *上面看不懂？没关系，从下面选你需要的看。*

### 我想知道每个命令是干什么的

| 我想... | 命令 | 举例 |
|---------|------|------|
| 开始一个需求 | `aegis start` | `aegis start "修bug"` |
| 看需求进度 | `aegis status` | `aegis status` |
| 检查当前阶段 | `aegis check` | `aegis check` |
| 推进到下一步 | `aegis advance` | `aegis advance` |
| 写开发日志 | `aegis devlog` | `aegis devlog write REQ-001 -m "完成了"` |
| 看完整帮助 | `aegis --help` | |

### 需求等级怎么选

| 等级 | 什么时候用 | 会走什么流程 |
|------|-----------|------------|
| L1 | 改个颜色、修个 typo | 登记 → 改代码 → DevLog → 完成 |
| L2 | 加新功能、优化模块 | 设计 → 实现 → DevLog → 完成 |
| L3 | 架构重构、大改 | 7 阶段全流程 |
| auto | 让系统自己判断 | `aegis start "标题" --level auto` |

### L2 需求完整流程示范

```bash
# 第 1 步：开始
aegis start "捕鱼炮台系统" --level L2

# 第 2 步：写设计文档（手动创建或用 AI 帮你写）
# 在 Aegis_Specs/L2/捕鱼炮台系统/design.md 写设计内容

# 第 3 步：检查
aegis check        # 应该全部通过

# 第 4 步：推进到实现
aegis advance

# 第 5 步：写代码...（你自己写）

# 第 6 步：写 DevLog
aegis devlog write REQ-001 -m "实现了炮台瞄准和发射"

# 第 7 步：完成
aegis advance      # 🎉 已完成
```

### 我想用 JSON 看状态（给脚本用）

```bash
aegis status --json
```

### 我想在 git commit 时自动检查

在你的项目目录下创建 `.pre-commit-config.yaml`：

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

然后运行：

```bash
pip install pre-commit
pre-commit install
```

之后每次 `git commit` 都会自动检查。不通过会阻断提交。

### 我还没装，怎么装

```bash
git clone https://github.com/Szy-Fxy/Aegis.git aegis-toolchain
cd aegis-toolchain
pip install -e .
aegis --help    # 验证安装
```

或者用一键脚本：
- Windows: 右键运行 `install.ps1`
- Mac/Linux: `bash install.sh`

### 出问题了怎么办

| 问题 | 试试这个 |
|------|---------|
| `aegis: command not found` | 重启终端。如果还不行，运行 `pip install -e .` 再试 |
| state.json 报错 | 删掉 `Aegis/state/state.json`，重新 `aegis start` |
| 一直卡住不动 | 可能另一个 aegis 在运行，关掉其他终端窗口 |
| 中文乱码 | PowerShell 用户：输入 `chcp 65001` 然后回车 |
