---
name: refactor-clean
description: Find and remove dead code, unused exports, duplicate modules, and unused dependencies inside a codebase. Use after workspace-hygiene-audit for per-repo cleanup, or when user asks refactor-clean, dead code, knip, unused files. Not for Cursor session folders or workspace root migration docs.
metadata:
  origin: ECC (refactor-cleaner agent, adapted for Cursor)
disable-model-invocation: true
---

# Refactor Clean (dead code)

Use **inside a single project repository** after structure is understood. Pair with `workspace-hygiene-audit` for folder-level work; use this for code-level cleanup.

## When to use

- Unused files, exports, dependencies in a JS/TS/Python repo
- Duplicate utilities after migration
- User explicitly requests refactor-clean or dead-code pass

## When NOT to use

- Auditing `~/.cursor/projects/var-folders-*` (Cursor internal — ignore)
- Deleting migration markdown at workspace root without `workspace-hygiene-audit` plan
- WSDC data paths under Tableau without explicit approval

## Detection (pick stack)

**Node/TS:**
```bash
npx knip
npx depcheck
npx ts-prune
```

**Python:**
```bash
# optional if installed
vulture .
find . -type d -name __pycache__ -not -path './.venv/*'
find . -name '*.pyc' -not -path './.venv/*'
```

## Workflow

1. **Analyze** — run tools; categorize SAFE / CAREFUL / RISKY
2. **Verify** — grep references, check public API, git history
3. **Remove in batches** — deps → exports → files; test after each batch
4. **Report** — what was removed, what remains risky

## Full ECC agent spec

Read [reference/refactor-cleaner.md](reference/refactor-cleaner.md) for detailed workflow and risk classes.

## Safety

- No behavior change without user approval
- Commit in small batches; never `git clean -fd` without explicit user request
