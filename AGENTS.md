# AI Agent Instructions

> This project uses **Aegis v3.1.0** — AI Development Governance System.

## BEFORE ANY CODE CHANGE

1. **Load the workflow engine**: `Aegis/skills/dev-workflow/SKILL.md`
2. **Classify the request**: L1 (trivial fix) / L2 (feature) / L3 (major refactor)
3. **L2 / L3**: Propose plan → get user approval → then code
4. **After each phase**: Write DevLog to `Aegis/rules/DevLogs/`

## Quick Self-Check (every response)

- [ ] What phase am I in? Updated `Aegis_Specs/INDEX.md`? Wrote DevLog?
- [ ] Any hardcoded credentials in my code?
- [ ] Did I expose production data or real secrets to AI?

## Core Rules

- Design before code (L2/L3)
- No hardcoded secrets — use `.env`
- Verify before closing — run tests, check acceptance criteria
- Always update `Aegis_Specs/INDEX.md`
- Every requirement (including L1) must be recorded in INDEX.md and DevLog

See `Aegis/docs/USER_GUIDE.md` for human documentation.