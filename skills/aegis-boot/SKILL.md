---
name: "aegis-boot"
description: "Aegis AI Development Governance System boot loader. Activates on any development task including: develop, create, modify, refactor, fix, implement, code, configure, requirement, feature, bug, optimize, test, deploy, build, design, review, debug, write, add, remove, update, change, improve."
---

# Aegis Boot

> This project uses **Aegis v3.0.5** AI Development Governance System.

## Activation

You've been activated because this task involves code changes.

### Before writing any code:

1. **Load the workflow engine**: `Aegis/skills/dev-workflow/SKILL.md`
2. **Classify the task**:
   - **L1**: trivial fix (typo, config change, single-line edit) — quick fix, still write DevLog and update INDEX
   - **L2**: feature / module / optimization — propose plan, get approval, then implement
   - **L3**: major refactor / architecture redesign — full 7-phase spec-driven workflow
3. **L2 / L3**: Propose plan → **wait for user approval** → implement
4. **After any change**: Write DevLog to `Aegis/rules/DevLogs/`

### Quick Rules

- No hardcoded secrets or credentials — use `.env`
- Design before code (L2 / L3)
- Always update `Aegis_Specs/INDEX.md`
- Every requirement (including L1) recorded in INDEX.md and DevLog
- Verify before closing — run tests, check acceptance criteria

### Anti-Patterns (DO NOT)

- Skip INDEX.md update even for L1
- Start coding before user approves the plan (L2 / L3)
- "While I'm here" cleanup of unrelated code
- Over-engineer: 200 lines that could be 50 → rewrite to 50