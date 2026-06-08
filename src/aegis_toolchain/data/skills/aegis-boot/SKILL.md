---
name: "aegis-boot"
description: "Aegis AI Development Governance System Boot Loader v5.2.1. MANDATORY activation on any code-related task. Activates on: develop, create, modify, refactor, fix, implement, code, configure, requirement, feature, bug, optimize, test, deploy, build, design, review, debug, write, add, remove, update, change, improve."
---

# Aegis Boot v5.2.1

> This project uses **Aegis v5.2.1** — AI Development Governance Toolchain.
> You are the AI. Use the `aegis` CLI tool for all state management.
> **Do not skip, reorder, or compress any step.**

---

## Activation — MANDATORY SEQUENCE

You've been activated because this task involves code changes. Execute the following steps **in order**. Every step is required.

### Step 1: Load Rules

**Before any other action**, read ALL of the following:

1. `Aegis/skills/dev-workflow/SKILL.md` — workflow engine (full L1/L2/L3 definitions)
2. `Aegis/rules/global.md` — global rules (SOLID, security, code style)
3. `Aegis/rules/TechStack/{tech-stack}.md` — tech stack rules (match to task)

### Step 2: Classify the Task

Use the classification table in the workflow engine. **Tell the user your classification** before proceeding:

- **L1**: Trivial fix — typo, config, single-line edit
- **L2**: Feature / module / optimization — needs a plan
- **L3**: Major refactor / architecture redesign — full 7-phase workflow

### Step 3: Execute the Classified Workflow

> **IMPORTANT**: Use the `aegis` CLI tool for ALL state management (register, advance, check, devlog).
> Do NOT manually edit INDEX.md, do NOT manually update phase status.
> INDEX.md 路径：`Aegis_Specs/INDEX.md`（由 `aegis init` 生成）。AI 不得在其他路径新建 INDEX.md。

---

#### L1 — Quick Fix

```
1. python -m aegis_toolchain start "需求名" -l L1     ← 自动登记到 INDEX.md（🔨 implementing）
2. Make the code change
3. Show change summary (file paths + lines added/removed + what changed)
   → wait for user confirmation
   → **DO NOT touch git/svn unless user explicitly asks**
4. python -m aegis_toolchain devlog write REQ-xxx -m "改动说明"   ← 自动写 DevLog
5. python -m aegis_toolchain advance                              ← 自动更新 INDEX.md 为 ✅ done
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] INDEX.md has entry for current requirement?
- [ ] INDEX.md status = ✅ done?
- [ ] DevLog written?

---

#### L2 — 5-Phase Sequence (DO NOT skip any phase)

##### L2-1: Design

```
Step 0: python -m aegis_toolchain start "需求名" -l L2   ← 自动登记到 INDEX.md（📐 design）
Step 1: Create Aegis_Specs/L2/{feature-name}/design.md using the template
Step 2: Present the plan to the user in chat
Step 3: Check acceptance criteria — are they in user's language (not technical)?
Step 4: WAIT for explicit user approval (e.g., "OK", "go ahead", "approved")
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] INDEX.md has entry for current requirement (status 📐 design)?
- [ ] design.md exists?
- [ ] Acceptance criteria in user language?
- [ ] User has explicitly confirmed?

**If any fails → STOP. Do not proceed to L2-2.**

##### L2-2: Design Review

```
Step 0: python -m aegis_toolchain advance               ← 自动更新 INDEX.md 为 📋 review_design
Step 1: Create Aegis_Specs/L2/{feature-name}/review.md (template: review-L2.md)
Step 2: Launch 4 sub-agents for design review (code-reviewer, devils-advocate, security-auditor, ux-reviewer)
Step 3: Summarize their output into review.md "设计审查" section
Step 4: Fix or document all findings before proceeding
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] review.md exists with "设计审查" section?
- [ ] 4 sub-agents have output?
- [ ] All findings fixed or documented?

**If any fails → fix before proceeding.**

##### L2-3: Implement

```
Step 0: python -m aegis_toolchain advance               ← 自动更新 INDEX.md 为 🔨 implementing
Step 1: Write code according to design.md
Step 2: Run typecheck / lint / build to verify
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] INDEX.md status = 🔨 implementing?
- [ ] Code compiles / passes lint?

**If any fails → fix before proceeding to L2-4.**

##### L2-4: Code Review

```
Step 0: python -m aegis_toolchain advance               ← 自动更新 INDEX.md 为 📋 review_code
Step 1: Launch 4 sub-agents for code review
Step 2: Append their output to review.md "代码审查" section
Step 3: Fix all findings before proceeding
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] review.md contains "代码审查" section?
- [ ] 4 sub-agents have output?
- [ ] All findings fixed?

##### L2-5: Verify

```
Step 0: python -m aegis_toolchain advance               ← 自动更新 INDEX.md 为 ✅ verify
Step 1: Create verify.md (template: verify-L2.md)
Step 2: Check every acceptance criterion from design.md
Step 3: Show change summary + verify.md to user → wait for confirmation
         (**DO NOT touch git/svn unless user explicitly asks**)
Step 4: python -m aegis_toolchain devlog write REQ-xxx -m "done"   ← 自动写 DevLog
Step 5: python -m aegis_toolchain advance                           ← 自动更新 INDEX.md 为 ✅ done
```

**BOUNDARY CHECK** (run `python -m aegis_toolchain check`):
- [ ] verify.md exists with all criteria checked?
- [ ] User confirmed?
- [ ] INDEX.md status = ✅ done?
- [ ] DevLog written?

---

#### L3 — Full 7-Phase Workflow

As defined in `Aegis/skills/dev-workflow/SKILL.md`. Use `python -m aegis_toolchain start`, `python -m aegis_toolchain advance`, `python -m aegis_toolchain check`, `python -m aegis_toolchain devlog write` instead of manual operations.

---

### Step 4: Phase Boundary Check (Mandatory)

Between **every** L2/L3 phase, run:

```
python -m aegis_toolchain check     ← 自动验证前置文件是否存在
```

If `python -m aegis_toolchain check` reports failures, fix the missing items before advancing.

---

## Failure Recovery

If you realize a phase was skipped or a file was not created:

```
STOP. Do not proceed.
Create the missing file(s).
Tell the user: "上一阶段缺少 [文件名]，已补创建。可以继续。"
Only then proceed.
```

---

## 版本号规则 (Version Numbering)

| 改动等级 | 版本升级规则 |
|---------|------------|
| **L1** — 小幅修改/修复 | PATCH +1 |
| **L2** — 功能/模块/优化 | MINOR +1, PATCH 归零 |
| **L3** — 架构重构/重大变更 | MAJOR +1, MINOR/PATCH 归零 |

**规则**：
- 每次改动完成后，根据本次改动的最高等级执行版本升级
- 自举模块（本文件）中的版本号必须与全局版本号保持一致

## Quick Rules

- No hardcoded secrets or credentials — use `.env`
- Design before code (L2 / L3)
- Always use `aegis` CLI for state management — never manually edit INDEX.md
- Every requirement (including L1) recorded via `python -m aegis_toolchain start`
- Verify before closing — run `python -m aegis_toolchain check`

## Anti-Patterns (DO NOT)

- Skip `python -m aegis_toolchain start` for any requirement (including L1)
- Start coding before user approves the plan (L2 / L3)
- "While I'm here" cleanup of unrelated code
- Over-engineer: 200 lines that could be 50 → rewrite to 50
- Manually edit INDEX.md — always use `python -m aegis_toolchain start / advance`
