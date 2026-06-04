# Aegis 自举规范

> **仅作用于 Aegis 仓库自身开发，不影响用户项目。**

Aegis 开发也遵循分级流程，但因为是内部开发，级别定义与用户场景不同。

---

## 分级定义

### A 级（小修小补）

- 修复 bug、编码问题、文档笔误
- 不涉及安装脚本行为变更
- 流程：**改代码 → 本地测试 → 提交**
- 提交信息格式：`vX.Y.Z Hotfix: 简短描述`

### B 级（功能新增 / 重构）

- 新增入口、新增模板、规则结构调整
- 影响安装脚本或用户可见行为
- 流程：**Plan → Approval → Code → Test → Review → 提交**
- 提交信息格式：`vX.Y.Z: 简短描述`

### C 级（重大架构变更）

- 目录结构变化、文件重命名、核心流程重构
- 影响所有用户
- 流程：**Spec → Design → Approval → Code → Full Test → 全文件审查 → 提交**
- 提交信息格式：`vX.Y.Z: 简短描述`

---

## 自举提交规范（强制执行）

每次改动完成后，按以下顺序执行：

```
1. 改代码
2. 本地 Test 目录安装验证
3. git diff 自查（确认无遗漏、无多余文件）
4. 全局版本号替换（如果版本号变了）
5. 更新 CHANGELOG.md
6. 更新 Aegis_Specs/INDEX.md（登记 REQ 记录）
7. git add -A
8. git commit -m "vX.Y.Z: 描述"
9. git tag -f vX.Y.Z HEAD
10. git push --force origin main vX.Y.Z
11. 视情况创建 GitHub Release（大版本必创建）
```

### 版本号集中管理

版本号出现位置（改动时全部更新）：

| 文件 | 位置 |
|------|------|
| `AGENTS.md` | 第 3 行 `Aegis vX.Y.Z` |
| `install.ps1` | 第 1 行注释 + 第 14 行 Write-Host |
| `install-aegis.ps1` | 第 3 行注释 + 第 41 行 Write-Host |
| `rules/global.md` | 版本号行 |
| `skills/aegis-boot/SKILL.md` | description 字段 + 标题 + 正文引用 |
| `skills/dev-workflow/SKILL.md` | 标题 + 版本日志 |
| `docs/Aegis_Intro.md` | 标题 + 版本日志 |
| `CHANGELOG.md` | 版本历史表 |

---

## 文件职责边界

| 文件 | 用途 | 安装到用户项目？ |
|------|------|:---:|
| `AGENTS.md` | AI 通用入口（安装时为模板） | ✅ 是 |
| `README.md` | GitHub 仓库首页 | ❌ 否（安装到 `Aegis/README.md`） |
| `CHANGELOG.md` | 集中版本日志 | ❌ 否 |
| `BOOTSTRAP.md` | 本文件，自举规范 | ❌ 否 |
| `install.ps1` | 远程一键安装脚本 | ❌ 否 |
| `install-aegis.ps1` | 本地跨 IDE 安装脚本 | ❌ 否 |
| `Aegis_Specs/INDEX.md` | 需求模板（空表） | ✅ 是 |
| `docs/` | 文档 | ✅ 是 |
| `rules/` | 规则引擎 | ✅ 是 |
| `skills/` | 技能文件 | ✅ 是 |

---

## 历史版本留存

- 每次发布打 tag：`vX.Y.Z`
- 不以 `--force` 覆盖已发布的 tag
- 历史版本 tag 永久保留，用户可通过 `https://github.com/Szy-Fxy/Aegis/archive/refs/tags/vX.Y.Z.zip` 下载
- GitHub Release 页面附版本说明