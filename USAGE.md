# Aegis Toolchain 使用指南

---

## 安装

### GitHub 安装

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

### 本地安装

```powershell
pip install D:\YourProject\aegis-toolchain
```

---

## 安装验证

安装完成后执行：

```powershell
aegis --help
```

正常情况下会显示 Aegis 命令帮助界面。

---

## Windows 常见问题

### 'aegis' 不是内部或外部命令

如果执行：

```powershell
aegis
```

出现：

```
'aegis' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

通常表示 Aegis 已成功安装，但 Python Scripts 目录尚未加入 PATH。

### 验证是否安装成功

直接执行：

```powershell
python -m aegis_toolchain --help
```

如果能够显示 Aegis 帮助信息，则说明安装成功，仅为 PATH 配置问题。

### 解决方案

Python Scripts 目录一般在 `%APPDATA%\Python\Python3XX\Scripts`（`3XX` 是你的 Python 版本号，如 `311`、`312`、`313`、`314`）。

将这个目录加入用户 PATH：

**方法 A（一劳永逸，推荐）**：

> ⚠️ 不要用 `setx PATH` 方式加 PATH——`setx` 有 1024 字符限制，PATH 过长时会静默截断，导致系统 PATH 损坏。

```powershell
# PowerShell（执行一次，永久生效）
$scripts = "$env:APPDATA\Python\Python314\Scripts"
$oldPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($oldPath -notlike "*$scripts*") {
    [Environment]::SetEnvironmentVariable("Path", "$oldPath;$scripts", "User")
}
```

```cmd
REM CMD（执行一次，永久生效）
set "scripts=%APPDATA%\Python\Python314\Scripts"
setx PATH "%PATH%;%scripts%"
```

> 如果你担心 PATH 截断风险，可以用 CMD 的 `setx` 但先备份当前 PATH：在 CMD 中执行 `echo %PATH% > %USERPROFILE%\path_backup.txt`。

执行完成后：
1. 关闭当前 CMD / PowerShell
2. 重新打开终端
3. 执行 `aegis --help` 即可正常使用

**方法 B（不折腾 PATH，每条命令加 `python -m`）**：

```powershell
# CMD / PowerShell 都通用
python -m aegis_toolchain init
python -m aegis_toolchain start "功能名称"
python -m aegis_toolchain check
```

### 查看 aegis 实际位置

```cmd
REM CMD
where aegis
```

```powershell
# PowerShell
Get-Command aegis
```

正常情况下应返回：

```
C:\Users\<用户名>\AppData\Roaming\Python\Python314\Scripts\aegis.exe
```

---

## 初始化项目

```powershell
cd D:\你的项目文件夹路径
aegis init
```

如果用的是方法 B，这里用：

```powershell
python -m aegis_toolchain init
```

---

## 验证初始化成功

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

## 命令速查

| 命令 | 说明 |
|------|------|
| `aegis init` | 初始化项目 Aegis 规则 |
| `aegis start <title> -l <L1\|L2\|L3>` | 开始新需求，自动分类和分配 ID |
| `aegis check` | 执行 BOUNDARY CHECK（边界检查） |
| `aegis advance` | 推进当前需求到下一阶段 |
| `aegis status` | 查看项目状态 |
| `aegis devlog write <id> -m <msg>` | 写开发日志 |
| `aegis devlog list` | 列出所有 DevLog |

---

## 卸载

```powershell
pip uninstall aegis-toolchain
```

## 升级

```powershell
pip install --upgrade git+https://github.com/Szy-Fxy/Aegis.git
```

升级工具链后，规则文件还是旧版本，需要同步到项目：

```powershell
cd D:\你的项目文件夹路径
aegis upgrade
```

`aegis upgrade` 会：
- 覆盖系统规则文件（备份原文件到 `Aegis/.backup/`）
- 跳过 TechStack 文件（你定制的部分保留不变）
- **不碰** DevLogs、state、TempData、Aegis_Specs、INDEX.md、AGENTS.md
