# Aegis v3.1.0 流程强化 — 开发日志

## 元信息

| 字段 | 值 |
|------|-----|
| 项目 | Aegis 自举 |
| 需求 | v3.1.0-feedback-improvements |
| 日期 | 2026-06-04 |
| 级别 | L2 |

## 改动摘要

### 修改文件 (5个)

| 文件 | 增/删行 | 改动 |
|------|---------|------|
| `skills/aegis-boot/SKILL.md` | +15 / -10 | L1/L2 流程：新增 INDEX.md 登记步骤（Step 0）；L2 新增验收标准用户视角检查；Boundary Check 全覆盖 |
| `skills/dev-workflow/SKILL.md` | +18 / -10 | 同上 + 反借口表补全；版本号 3.0.7→3.1.0 |
| `skills/dev-workflow/templates/spec-L2.md` | +10 / -2 | 标题改为「L2 方案设计模板」；新增方案风险边界 section |
| `skills/dev-workflow/templates/design.md` | +8 / -0 | 新增方案风险边界 section |
| `skills/dev-workflow/templates/proposal.md` | +8 / -0 | 新增方案风险边界 section |

### 版本号更新 (8个文件)

`global.md`, `AGENTS.md`, `README.md`, `Aegis_Intro.md`, `install.ps1`, `install-aegis.ps1`, `CHANGELOG.md`, `aegis-boot/SKILL.md` — 全部 v3.0.7 → v3.1.0

## 当前进度

- L2-1 方案设计 ✅完成
- L2-2 实现 ✅完成
- L2-3 验证 + 收尾 ✅完成

## 关键决策

- INDEX.md 登记步骤嵌入 L2-1 Step 0（而非全局规则），确保流程入口可执行
- 验收标准用户视角检查放在 L2-1 展示方案之后、等确认之前，作为最后一道防线
- 方案风险边界至少 2 个场景，不可为空，防止走过场
- L1 同样需要登记 INDEX.md，防止 L1 也被遗漏

## 下一动作

- 推送到 GitHub → 创建 tag v3.1.0