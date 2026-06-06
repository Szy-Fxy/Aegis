# Aegis Toolchain 使用指南

---

## 完整安装流程（全部在 CMD 或 PowerShell 里完成）

> 下面每一步都是一条命令，复制粘贴进去按回车就行。

### 1. 安装 Python（如果没有的话）

```powershell
winget install -e --id Python.Python.3.14
```

> 如果你电脑上已经有 Python，这条命令会提示"已安装"，直接下一步。

### 2. 刷新 PATH + 安装 Aegis

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","User") + ";" + [Environment]::GetEnvironmentVariable("Path","Machine"); pip install git+https://github.com/Szy-Fxy/Aegis.git
```

> 第一段 `$env:Path = ...` 是刷新环境变量，让系统找到刚装的 Python 和 pip。
> 装了 Python 后一定要关掉 CMD 重新打开，或者运行这条刷新命令，否则 `pip` 找不到。

### 3. 进入你的项目并初始化

```powershell
cd D:\你的项目文件夹路径
aegis init
```

---

## 验证安装成功

装完后运行这几条命令，全部正常输出就说明好了：

```powershell
aegis --help
```

应该显示：

```
 Usage: aegis [OPTIONS] COMMAND [ARGS]...
 Aegis 开发治理工具链 v5.0.0 — 让流程约束从 AI 自律转向工具强制
```

```powershell
aegis status
```

如果显示 `暂无需求记录` 就说明一切正常。

---

## 开始开发

打开 Hana（或其他 AI 工具），打开你的项目文件夹，然后像平时一样和 AI 对话。

你只需要说需求，AI 会自动：
- 判断任务是简单修复（L1）还是功能开发（L2）还是架构重构（L3）
- 写设计文档 → 调子代理审查设计方案 → 写代码 → 调子代理审查代码 → 你确认验收
- 每一步完成后会告诉你结果，需要你确认时会问你

---

## 碰见问题了？

| 现象 | 原因 | 解决 |
|------|------|------|
| `winget` 不是内部或外部命令 | Windows 版本太低，没有自带 winget | 打开 https://python.org 下载安装，勾上 "Add Python to PATH" |
| `'pip' 不是内部或外部命令` | Python 装完后没刷新 PATH | 关掉 CMD 重新打开，或运行上面的刷新命令 |
| `'aegis' 不是内部或外部命令` | 装完没重启 CMD | 关掉 CMD 重新打开 |
| `aegis init` 后文件不全 | 初始化被中断 | 重新运行 `aegis init --force` |
| 中文显示乱码 | 终端编码不对 | 在 CMD 里输入 `chcp 65001` 回车 |
