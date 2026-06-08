# Aegis Toolchain 使用指南

---

## 完整安装流程

> 前置条件：Python 3.11+ 和 Git。如果还没有 Python，先去 [python.org](https://python.org) 下载安装。

### 1. 安装 Aegis

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

### 2. 把 `aegis` 命令加到 PATH（Windows 用户必看）

pip 安装完会把 `aegis.exe` 放进一个 Scripts 目录，但这个目录**不一定在系统 PATH 里**。
如果直接敲 `aegis` 报"不是内部或外部命令"，说明需要加 PATH。

**方法 A（一劳永逸，推荐）：**

```powershell
# 把 Scripts 目录加到用户 PATH（执行一次，永久生效）
$scripts = "$env:USERPROFILE\AppData\Roaming\Python\Python314\Scripts"
[Environment]::SetEnvironmentVariable("Path", `
    [Environment]::GetEnvironmentVariable("Path", "User") + ";" + $scripts, "User")
# 关掉终端重新打开，之后就能直接敲 aegis 了
```

**方法 B（不折腾 PATH，每条命令加 `python -m`）：**

```powershell
# 效果完全一样，只是每次要多打几个字
python -m aegis_toolchain init
python -m aegis_toolchain start "功能名称"
python -m aegis_toolchain check
```

### 3. 进入项目并初始化

```powershell
cd D:\你的项目文件夹路径
aegis init
```

如果上一步选了方法 B，这里用：

```powershell
python -m aegis_toolchain init
```

---

## 验证安装成功

```powershell
aegis --help
```

应该显示：

```
 Usage: aegis [OPTIONS] COMMAND [ARGS]...
 Aegis 开发治理工具链 v5.2.0 — 让流程约束从 AI 自律转向工具强制
```

```powershell
aegis status
```

如果显示 `暂无需求记录` 就说明一切正常。

---

## 快速上手示例

以下演示一个 L2 需求的完整生命周期：

```powershell
# 1. 登记需求
aegis start "添加背包系统" -l L2

# 2. 写设计文档 → 检查
aegis check

# 3. 推进到下一阶段
aegis advance  # design → review_design

# 4. 继续写代码、检查、推进...
aegis check
aegis advance  # review_design → implementing

# 5. 写 DevLog
aegis devlog write REQ-001 -m "完成了背包 UI 和数据结构"

# 6. 推进到 done
aegis advance
```

---

## 命令详解

| 命令 | 说明 |
|------|------|
| `aegis start <title> -l <L1\|L2\|L3>` | 开始新需求，自动分类和分配 ID |
| `aegis check` | 执行 BOUNDARY CHECK（边界检查） |
| `aegis advance` | 推进当前需求到下一阶段 |
| `aegis status` | 查看项目状态 |
| `aegis devlog write <id> -m <msg>` | 写开发日志 |
| `aegis devlog list` | 列出所有 DevLog |
| `aegis init` | 初始化项目 Aegis 规则 |

---

## 常见问题

| 症状 | 原因 | 解决 |
|------|------|------|
| `'aegis' 不是内部或外部命令` | pip 的 Scripts 目录不在 PATH 里 | 加 PATH（见上面第 2 步）或改用 `python -m aegis_toolchain` |
| `'python' 不是内部或外部命令` | Python 没装或没加 PATH | 装 Python 3.11+ 并勾选"Add Python to PATH" |
| `未找到 state.json` | 还没 `aegis init` | 在当前项目目录运行 `aegis init` |
