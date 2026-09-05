---
name: workspace-hygiene-audit
description: Read-only audit of Cursor workspace folder structure, projects, logs, legacy artifacts, and duplicates. Classify items as keep, archive, relocate, or delete-candidate. Use when user wants project cleanup, folder order, phantom logs, migration clutter, or workspace audit. Never delete without explicit user approval per item list.
metadata:
  scope: "~/.cursor workspace"
---

# Workspace Hygiene Audit

Audit **folder structure and artifacts** in the Cursor workspace. Complements `project-organization.mdc` (standards) and `refactor-clean` (dead code inside repos).

**Default mode: read-only report.** No moves, no deletes unless user approves a numbered action list.

## Workspace map (this machine)

```
~/.cursor/                          # workspace root (git repo)
├── projects/                       # ALL real code projects — audit here
│   ├── tableau/     (~7.8G — check data vs artifacts)
│   ├── python/      (~4.6G)
│   ├── wsdc/
│   ├── job-search/  (career OS — not python/job-scraper)
│   ├── data-analysis/
│   └── learning/
├── archive/                        # legacy scripts, temp files, old docs
├── config/                         # mcp.json — never delete
├── docs/                           # workspace docs + audit reports
├── skills/                         # ~/.cursor/skills
├── logs/                           # hooks-audit.jsonl
├── hooks/
└── *.md at root                    # migration reports → ARCHIVE candidate
```

### IGNORE (do not classify as user projects)

| Pattern | Reason |
|---------|--------|
| `~/.cursor/projects/var-folders-*` | Cursor session/MCP cache |
| `~/.cursor/projects/<numeric-id>/` | Chat session metadata (canvases, terminals) |
| `~/.cursor/projects/Users-*` | Cursor project binding metadata |
| `.venv/`, `node_modules/`, `.git/` inside projects | Dependencies — don't delete |
| `projects/tableau/.../WSDC Points/` | Critical shared data path |

## When to activate

- "навести порядок", "аудит проектов", "странные папки", "phantom logs"
- "что удалить", "legacy", "migration clutter", "workspace audit"
- Before large migration or after months of ad-hoc files

## Related skills

| Skill | Role |
|-------|------|
| **This skill** | Folder/tree audit, logs placement, duplicates, archive plan |
| `workspace-surface-audit` | MCP, hooks, skills inventory (harness layer) |
| `skill-stocktake` | Quality audit of `~/.cursor/skills/` only |
| `refactor-clean` | Dead code inside one repo after structure is fixed |
| `project-setup` | Scaffold new projects to standard |
| `search-first` | Before writing new utility — reuse existing |

Always read **`.cursor/rules/project-organization.mdc`** for target structure.

## Phase 0 — Scope

Confirm with user (or infer from message):

1. **Scope path** — full `~/.cursor` vs `projects/` only vs one category (`python/`, `tableau/`)
2. **Depth** — top-level inventory vs per-project deep dive
3. **Actions allowed** — report-only (default) vs move/archive after approval

## Phase 1 — Inventory

Run read-only commands; collect evidence:

```bash
# Top-level projects (real)
ls -la ~/.cursor/projects/ | grep -vE 'var-folders|^[0-9]+$'

# Size hotspots
du -sh ~/.cursor/projects/* 2>/dev/null | sort -hr | head -20

# Root markdown clutter
find ~/.cursor -maxdepth 1 -name '*.md' -type f

# Logs outside logs/
find ~/.cursor/projects -name '*.log' -o -name '*.jsonl' 2>/dev/null | grep -v node_modules | grep -v .venv | head -50

# Duplicate project names
find ~/.cursor/projects -maxdepth 2 -type d -name 'job-search' 2>/dev/null
```

Also check: `PROJECTS.md` vs actual paths, `archive/` usage, per-project `README.md` presence.

## Phase 2 — Classify every finding

Use exactly one label per item:

| Label | Meaning | Typical action |
|-------|---------|----------------|
| **KEEP** | Active, correctly placed | None |
| **RELOCATE** | Valid file, wrong folder | Move to `logs/`, `data/`, `docs/`, `archive/` |
| **ARCHIVE** | Legacy but might be needed | `archive/` with date subfolder |
| **MERGE** | Duplicate project/split brain | Consolidate + README pointer |
| **DELETE-CANDIDATE** | Safe to remove after confirm | User approval only |
| **IGNORE** | Cursor internal / generated | Never touch |

### Log hygiene rules

- Per-project logs → `<project>/logs/` (gitignore if ephemeral)
- Workspace hooks log → `~/.cursor/logs/`
- No `*.log` in project root (flag **RELOCATE**)
- Tableau/WSDC parser logs near data → prefer `logs/` subfolder next to scripts, not mixed with CSV

### Known split-brain (verify in audit)

- `projects/job-search/` — career OS (`career/`)
- `projects/python/job-scraper/` — scraper/parser (renamed from `job-search`; README cross-link to career OS)

## Phase 3 — Report (required output)

Write markdown report (path: `docs/workspace-audit-YYYY-MM-DD.md` or user-specified):

```markdown
# Workspace Hygiene Audit — YYYY-MM-DD

## Scope
...

## Summary
- KEEP: N | RELOCATE: N | ARCHIVE: N | MERGE: N | DELETE-CANDIDATE: N | IGNORE: N
- Estimated recoverable space (if measured): ...

## Top issues (priority order)
1. ...

## Inventory by area
### ~/.cursor root
| Path | Size | Class | Notes |

### projects/python
...

## Relocate plan
| From | To | Risk |

## Archive plan
| From | To | Risk |

## Delete candidates (requires explicit YES)
| Path | Reason | Verified unused? |

## Merge / dedupe plan
...

## Do NOT touch
- WSDC Points path
- var-folders-*
- config/github tokens
...

## Recommended next session commands
(paste prompts for execution phase)
```

## Phase 4 — Execution (only after user approval)

Order:

1. **ARCHIVE** root migration `*.md` → `archive/docs/migration-2025/` (low risk)
2. **RELOCATE** logs into `logs/`
3. **MERGE** READMEs / update `PROJECTS.md`
4. **DELETE-CANDIDATE** one batch at a time with `git status` check
5. Per-repo **refactor-clean** if dead code remains

Never run: `rm -rf`, `git clean -fd`, delete `var-folders-*`, delete data directories without user naming each path.

## Phase 5 — Verify

- `PROJECTS.md` matches disk
- Each active project has `README.md`
- No new `*.log` in project roots (spot check)
- User confirms critical paths still work (bot, Tableau, WSDC)

## Pair with harness audit

If user also wants MCP/skills/hooks inventory, run **`workspace-surface-audit`** in a second pass (or same report, separate section).
