# Aegis

This project uses **Aegis AI Development Governance Toolchain**.
All code changes follow a governed workflow: classify → design → review → implement → verify.

## For AI Assistants

Before any code change, you MUST:

1. Read `Aegis/skills/aegis-boot/SKILL.md` for the full workflow
2. Use `python -m aegis_toolchain start "<requirement>"` to register and auto-classify (L1/L2/L3)
3. Follow the classified level workflow:
   - **L1**: Quick fix (typo, single-line, config) — fix directly
   - **L2**: Feature / module / optimization — design → implement → verify
   - **L3**: Major refactor / architecture — full workflow with review gates

## Quick Start

```bash
python -m aegis_toolchain status                    # View current project state
python -m aegis_toolchain start "<title>" -l L2    # Start a new requirement
python -m aegis_toolchain check                     # Run boundary check
python -m aegis_toolchain advance                   # Advance to next phase
```

**All state is tracked in `Aegis/state/state.json` and `Aegis_Specs/INDEX.md`.**
