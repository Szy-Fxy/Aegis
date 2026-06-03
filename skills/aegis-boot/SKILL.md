---
name: "aegis-boot"
description: "Aegis AI Development Governance System Boot Loader v3.0.6. MANDATORY activation on any code-related task. Activates on: develop, create, modify, refactor, fix, implement, code, configure, requirement, feature, bug, optimize, test, deploy, build, design, review, debug, write, add, remove, update, change, improve."
---

# Aegis Boot v3.0.6

> This project uses **Aegis v3.0.6** — AI Development Governance System.
> You are the AI. This is your mandatory activation sequence.
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

---

#### L1 — Quick Fix

```
1. Write DevLog → Aegis/rules/DevLogs/
2. Update INDEX → Aegis_Specs/INDEX.md
3. Make the code change
4. Show change summary (file paths + lines added/removed + what changed)
   → wait for user confirmation
   → **DO NOT touch git/svn unless user explicitly asks**
```

**BOUNDARY CHECK**: `Aegis_Specs/INDEX.md` updated ✅ + DevLog written ✅

---

#### L2 — 3-Phase Sequence (DO NOT skip any phase)

##### L2-1: Design

```
Step 1: Create Aegis_Specs/L2/{feature-name}/design.md using the template
Step 2: Present the plan to the user in chat
Step 3: WAIT for explicit user approval (e.g., "OK", "go ahead", "approved")
```

**BOUNDARY CHECK** (use `read` tool to verify):
- [ ] `Aegis_Specs/L2/{feature-name}/design.md` exists?
- [ ] User has explicitly confirmed?

**If either fails → STOP. Do not proceed to L2-2.**

##### L2-2: Implement

```
Step 1: Write code according to design.md
Step 2: Run typecheck / lint / build to verify
Step 3: Show change summary (file paths + lines added/removed + what changed)
Step 4: Wait for user confirmation
        → **DO NOT touch git/svn unless user explicitly asks**
```

**BOUNDARY CHECK** (use `read` tool to verify):
- [ ] Code compiles / passes lint?
- [ ] Change summary shown to user?

**If either fails → fix before proceeding to L2-3.**

##### L2-3: Verify & Close

```
Step 1: Update Aegis_Specs/INDEX.md (mark as ✅ done)
Step 2: Write DevLog to Aegis/rules/DevLogs/
Step 3: Tell user the task is complete
```

**BOUNDARY CHECK** (use `read` tool to verify):
- [ ] `Aegis_Specs/INDEX.md` updated?
- [ ] `Aegis/rules/DevLogs/` has new entry?

**If either fails → complete before declaring done.**

---

#### L3 — Full 7-Phase Workflow

As defined in the workflow engine (`Aegis/skills/dev-workflow/SKILL.md`). Each phase requires its own boundary check. Sub-agents must be invoked in L3-6.

---

### Step 4: Phase Boundary Check (Mandatory)

Between **every** L2/L3 phase, stop and verify:

```
□ Does the previous phase's required file exist? (use `read` tool to confirm)
□ Missing file → fall back to previous phase, create the file, do NOT advance
□ All files present → proceed to next phase
```

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

## Quick Rules

- No hardcoded secrets or credentials — use `.env`
- Design before code (L2 / L3)
- Always update `Aegis_Specs/INDEX.md`
- Every requirement (including L1) recorded in INDEX.md and DevLog
- Verify before closing — run tests, check acceptance criteria

## Anti-Patterns (DO NOT)

- Skip INDEX.md update even for L1
- Start coding before user approves the plan (L2 / L3)
- "While I'm here" cleanup of unrelated code
- Over-engineer: 200 lines that could be 50 → rewrite to 50
- Present plan in chat without creating the design.md file first
- Skip BOUNDARY CHECK — it's the only thing preventing phase-skipping