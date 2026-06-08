# Aegis

This project uses **Aegis AI Development Governance Toolchain**.
All code changes follow a governed workflow: classify → design → review → implement → verify.

## For AI Assistants

Before any code change, you MUST:

1. Read `Aegis/skills/aegis-boot/SKILL.md` for the full workflow
2. Run `aegis preprocess "<user message>"` to get classified instructions
3. Follow the appropriate level:
   - **L1**: Quick fix (typo, single-line, config) — fix directly
   - **L2**: Feature / module / optimization — design → review → implement → verify
   - **L3**: Major refactor / architecture — full 7-phase workflow

## Quick Start

```bash
aegis status                   # View current project state
aegis start "<title>" -l L2   # Start a new requirement
aegis check                    # Run boundary check
```
