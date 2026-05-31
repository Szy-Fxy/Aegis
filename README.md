# Aegis — 项目入口

> 本目录是 Aegis v3.0 核心，可跨项目、跨 IDE 复制使用。
> AI 请按 `skills/dev-workflow/SKILL.md` 自动加载对应规则。

---

## 🚀 快速开始

人类用户请看：[QUICK_START.md](QUICK_START.md)（30 秒）或 [USER_GUIDE.md](USER_GUIDE.md)（5 分钟）

---

## 规则文件索引

| 文件 | 用途 | 触发条件 |
|------|------|----------|
| [rules/global.md](rules/global.md) | 全局通用准则 | 始终加载 |
| [rules/TechStack/python.md](rules/TechStack/python.md) | Python 规范 | Python 相关需求 |
| [rules/TechStack/unity.md](rules/TechStack/unity.md) | Unity / C# 规范 | Unity 相关需求 |
| [rules/TechStack/typescript.md](rules/TechStack/typescript.md) | TypeScript / Node.js 规范 | TS/Web 相关需求 |
| [rules/TechStack/unreal.md](rules/TechStack/unreal.md) | Unreal Engine 规范 | UE 相关需求 |
| [rules/TechStack/cpp.md](rules/TechStack/cpp.md) | 通用 C++ 规范 | 非 UE 的 C++ 需求 |
| [rules/TempData/](rules/TempData/) | 开发中临时参考资料 | 技术调研时自动使用 |
| [rules/DevLogs/](rules/DevLogs/) | 开发日志存档 | 功能完成后自动写入 |

---

## 工作流

所有需求遵循 [skills/dev-workflow/SKILL.md](skills/dev-workflow/SKILL.md) 的 L1 / L2 / L3 分级流程。

---

## 安装到新项目

```powershell
# 在新项目根目录运行：
.\Aegis\install-aegis.ps1 -TechStack unity,python
```

或手动复制整个 `Aegis/` 文件夹到新项目根目录。

---

## 现有技术栈文件

如果遇到的技术栈不在上述列表中，AI 应按照 SKILL.md 中的「技术栈文件不存在时」流程：
搜索 → 审查 → TempData 暂存 → 生成新 TechStack 文件。