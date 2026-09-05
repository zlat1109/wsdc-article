# GSD Commands Reference

Complete reference for all GSD commands with examples and edge cases.

---

## Core Workflow Commands

### `gsd init`

Initialize a new GSD project.

**Syntax**: `gsd init`

**Process**:
1. Ask 5 focused questions
2. Optional: Research domain (if unfamiliar)
3. Generate initial files

**Questions**:
- "Describe your project in 2-3 sentences"
- "What's the core problem this solves?"
- "Who is this for?"
- "What's your tech stack?"
- "What does 'done' look like for v1.0?"

**Generated files**:
```
.gsd/
├── PROJECT.md         # Vision, tech stack, constraints
├── REQUIREMENTS.md    # Detailed requirements
├── ROADMAP.md         # All phases
└── STATE.md           # Current state
```

**Example**:
```bash
$ gsd init

> Describe your project in 2-3 sentences
A task management API for remote teams. Users can create projects,
assign tasks, track progress, and get notifications.

> What's the core problem this solves?
Remote teams struggle with scattered tasks across email, Slack, and docs.
This centralizes everything.

> Who is this for?
Small remote teams (5-20 people), primarily engineering and product teams.

> What's your tech stack?
Python 3.11, FastAPI, PostgreSQL, Redis

> What does 'done' look like for v1.0?
- Users can CRUD projects and tasks
- Real-time notifications work
- 95%+ uptime
- < 200ms API response time

✓ Project initialized!
  - .gsd/PROJECT.md
  - .gsd/REQUIREMENTS.md
  - .gsd/ROADMAP.md (6 phases)
  - .gsd/STATE.md

Next: Run `gsd discuss 1` to begin Phase 1
```

**Edge cases**:
- Existing .gsd/ folder → Ask if should overwrite or merge
- No clear tech stack → Suggest based on project type
- Vague requirements → Ask clarifying questions

---

### `gsd discuss [N]`

Clarify requirements for phase N.

**Syntax**: `gsd discuss [phase-number]`

**Arguments**:
- `[phase-number]`: Required. Which phase to discuss (e.g., 1, 2, 3)

**Process**:
1. Load: PROJECT.md, ROADMAP.md (phase N), STATE.md
2. Summarize phase goal
3. Identify gray areas
4. Ask clarifying questions
5. Document decisions in CONTEXT.md

**Critical**: NO CODE during discuss. Only conversation.

**Example**:
```bash
$ gsd discuss 1

Phase 1: Database Setup & Core Models

Goal: Set up PostgreSQL database with users, projects, and tasks tables.

Let me clarify a few things:

1. User authentication: Should we store passwords (hashed)
   or use OAuth only?

2. Task relationships: Can a task belong to multiple projects?

3. Soft deletes: Should deleted projects/tasks be archived or
   hard deleted?

> 1. Store passwords with bcrypt, OAuth is Phase 3
> 2. One project per task only
> 3. Soft deletes - keep audit trail

Understood. A few edge cases:

1. What happens when project deleted but has tasks?
2. Max task description length?
3. Task priority levels?

> 1. Cascade delete the tasks (soft delete both)
> 2. 10,000 characters
> 3. Low/Medium/High/Urgent (enum)

Perfect! Documenting decisions...

✓ Phase 1 discussion complete
  - .gsd/phases/phase-1/CONTEXT.md created

Next: Run `gsd plan 1` to create task plan
```

**CONTEXT.md output**:
```markdown
# Phase 1 Context

## Decisions
- **Authentication**: Store hashed passwords (bcrypt), OAuth deferred to Phase 3
- **Task-Project relationship**: One-to-one, no multi-project tasks
- **Deletions**: Soft delete with cascade (project deletion soft-deletes tasks)
- **Task description**: Max 10,000 characters
- **Priority levels**: Enum: Low, Medium, High, Urgent

## Out of Scope
- OAuth integration - Phase 3
- Task dependencies - Phase 5
- File attachments - Phase 6

## Edge Cases
- Project with tasks deleted → Cascade soft delete all tasks
- Task description > 10k chars → Validation error at API level
- Null priority → Default to Medium

## Open Questions
None - all clarified during discussion
```

**Edge cases**:
- Phase already has CONTEXT.md → Ask if should update or start fresh
- Phase not in ROADMAP.md → Error, show available phases
- No ROADMAP.md → Error, run `gsd init` first

---

### `gsd plan [N]`

Create atomic task plan for phase N.

**Syntax**: `gsd plan [phase-number] [--skip-research]`

**Arguments**:
- `[phase-number]`: Required. Which phase to plan
- `--skip-research`: Optional. Skip research subagent even for complex topics

**Process**:
1. Load: PROJECT.md (tech), ROADMAP.md (phase N), CONTEXT.md, previous SUMMARY.md
2. Optional: Spawn research subagent
3. Break phase into 2-3 atomic tasks
4. Create PLAN-X.md files using XML format
5. Validate plans

**Example**:
```bash
$ gsd plan 1

Planning Phase 1: Database Setup & Core Models

Based on discussion, breaking into 3 tasks:

Task 1: Database schema and migrations
  - Create users, projects, tasks tables
  - Add soft delete support (deleted_at column)
  - Create indexes

Task 2: SQLAlchemy models
  - Define models matching schema
  - Add relationships and constraints
  - Include validation

Task 3: Database utilities
  - Connection pooling
  - Migration runner
  - Seed data script

✓ Plans created:
  - .gsd/phases/phase-1/PLAN-1.md (Database schema)
  - .gsd/phases/phase-1/PLAN-2.md (SQLAlchemy models)
  - .gsd/phases/phase-1/PLAN-3.md (Utilities)

Next: Run `gsd execute 1` to implement
```

**With research**:
```bash
$ gsd plan 4

Planning Phase 4: Real-time notifications

This phase involves WebSockets. Spawning research subagent...

Researcher investigating:
- WebSocket libraries for FastAPI
- Connection management at scale
- Message queuing options

✓ Research complete: .gsd/phases/phase-4/RESEARCH.md

Recommendation: Use fastapi-websocket-rpc + Redis pub/sub

Creating task plans...
```

**Edge cases**:
- No CONTEXT.md → Warn that discussing first is recommended
- Phase already has PLAN files → Ask if should overwrite
- Very complex phase → Suggest splitting into multiple phases

---

### `gsd execute [N]`

Execute tasks for phase N with fresh context.

**Syntax**: `gsd execute [phase-number] [--skip-verify] [--parallel]`

**Arguments**:
- `[phase-number]`: Required. Which phase to execute
- `--skip-verify`: Optional. Skip post-task verification (not recommended)
- `--parallel`: Optional. Run independent tasks in parallel

**Process**:
For each task:
1. Clear context
2. Load: PROJECT.md (tech), PLAN-X.md, relevant files
3. Implement according to plan
4. Self-verify against acceptance criteria
5. Commit with conventional format
6. Announce completion
7. Repeat for next task

**Example**:
```bash
$ gsd execute 1

Executing Phase 1: Database Setup & Core Models

---
Starting Task 1: Database schema and migrations

Loading fresh context:
- PROJECT.md (tech stack)
- PLAN-1.md
- (no existing files, creating new)

Implementing...
- Created migrations/001_init.sql
- Created migrations/002_add_soft_delete.sql
- Created migrations/003_indexes.sql

Self-verification:
✓ Tables created successfully
✓ Soft delete columns present
✓ Indexes created

Committing...
[feat(phase-1) 8a3d9e2] feat(phase-1): add database schema
 3 files changed, 145 insertions(+)

✓ Task 1 complete: Database schema and migrations implemented
---

Clearing context for Task 2...

Loading fresh context:
- PROJECT.md (tech stack)
- PLAN-2.md
- migrations/001_init.sql (for reference)

Starting Task 2: SQLAlchemy models
...
```

**Parallel execution**:
```bash
$ gsd execute 5 --parallel

Phase 5 has independent tasks 1 and 2. Running in parallel...

[Task 1] Starting: API endpoint tests
[Task 2] Starting: UI component tests

[Task 1] ✓ Complete
[Task 2] ✓ Complete

Task 3 depends on 1 and 2. Running sequentially...
```

**Edge cases**:
- No PLAN files → Error, run `gsd plan N` first
- Git dirty working directory → Ask if should stash or commit existing changes
- Task fails verification → Stop, don't proceed to next task

---

### `gsd verify [N]`

Verify deliverables for phase N.

**Syntax**: `gsd verify [phase-number]`

**Arguments**:
- `[phase-number]`: Required. Which phase to verify

**Process**:
1. Load: ROADMAP.md (goals), all PLAN-X.md, STATE.md
2. Extract verification commands from plans
3. Run automated tests
4. Provide manual verification instructions
5. Document results
6. Suggest next action

**Example**:
```bash
$ gsd verify 1

Verifying Phase 1: Database Setup & Core Models

### Automated Tests
Running: pytest tests/ -v
✓ test_database_connection ... PASSED
✓ test_create_user ... PASSED
✓ test_soft_delete_user ... PASSED
✓ test_cascade_delete_project ... PASSED
All 24 tests passed

Running: mypy src/
✓ No type errors found

### Manual Verification

Please verify:
1. Connect to database: psql -d taskmanager
2. Check tables: \dt
   Expected: users, projects, tasks, migrations

3. Check soft delete column: \d users
   Expected: deleted_at column present

4. Test cascade delete:
   - Create project with tasks
   - Soft delete project
   - Verify tasks also soft deleted

Mark as complete: [y/n]
> y

### Verification Results
✓ Automated tests: PASS
✓ Manual checks: PASS (user confirmed)

Overall: PASS

Next: Run `gsd complete 1` to finalize phase
```

**Edge cases**:
- Tests fail → Show which task likely failed, suggest re-executing that task
- Manual checks unclear → Ask user to describe what they see
- No verification commands in plans → Create basic verification from acceptance criteria

---

### `gsd complete [N]`

Mark phase N as complete.

**Syntax**: `gsd complete [phase-number]`

**Arguments**:
- `[phase-number]`: Required. Which phase to mark complete

**Process**:
1. Generate SUMMARY.md
2. Update STATE.md (mark phase complete, advance to N+1)
3. Update ROADMAP.md (mark requirements done)
4. Optional: Create git tag

**Example**:
```bash
$ gsd complete 1

Completing Phase 1...

✓ Created .gsd/phases/phase-1/SUMMARY.md
✓ Updated STATE.md (current phase: 2)
✓ Updated ROADMAP.md (phase 1 requirements marked complete)

Phase 1 complete! ✓

Summary:
- Tasks completed: 3/3
- Commits: 3
- Files changed: 12
- Tests added: 24

Next: Run `gsd discuss 2` to begin Phase 2 (API Endpoints)
```

**SUMMARY.md**:
```markdown
# Phase 1 Complete ✓

**Completed**: 2026-01-31

## What Was Built
- PostgreSQL database schema (users, projects, tasks)
- Soft delete support with cascade
- SQLAlchemy models with validation
- Database utilities and migrations

## Files Changed
- migrations/001_init.sql - Initial schema
- migrations/002_add_soft_delete.sql - Soft delete support
- migrations/003_indexes.sql - Performance indexes
- src/db/models.py - SQLAlchemy models
- src/db/connection.py - DB connection pooling
- src/db/migrations.py - Migration runner

## Decisions Made
- Used bcrypt for password hashing (cost factor: 12)
- Connection pool: min 5, max 20 connections
- Alembic for migrations (over raw SQL for complex changes)

## Metrics
- Tasks: 3
- Commits: 3
- Files: 12
- Lines of code: ~500
- Tests: 24

## Notes for Future Phases
- Database connection string in .env (not committed)
- Migration order matters - run sequentially
- Soft delete filter should be applied in API layer
```

**Edge cases**:
- Phase not verified yet → Warn, ask if should complete anyway
- Phase already complete → Error, show state
- Next phase doesn't exist → Suggest creating new phase or project complete

---

### `gsd status`

Show current project state.

**Syntax**: `gsd status`

**Example**:
```bash
$ gsd status

# GSD Status

**Project**: Task Management API
**Phase**: 2 - API Endpoints
**Status**: Executing (Task 2 of 3)

## Progress
[■■□□□□] 33% (2/6 phases complete)

## Completed Phases
- Phase 1: Database Setup ✓ (2026-01-30)
- Phase 2: API Endpoints ✓ (2026-01-31)

## Current Phase (3: Authentication)
- [x] Task 1: JWT utilities
- [ ] Task 2: Login/logout endpoints ← YOU ARE HERE
- [ ] Task 3: Protected route middleware

## Next Action
`gsd execute 3` (continue with task 2)

## Recent Decisions
- Use jose for JWT (not PyJWT) - better type hints
- Access token: 15 min, refresh token: 7 days
- Store refresh tokens in Redis

## Blockers
None

## Stats
- Total commits: 8
- Total tests: 47
- Days active: 2
```

**Edge cases**:
- No .gsd/ folder → Error, run `gsd init`
- STATE.md corrupted → Try to reconstruct from other files

---

## Phase Management Commands

### `gsd add-phase`

Add a new phase to roadmap.

**Syntax**: `gsd add-phase`

**Example**:
```bash
$ gsd add-phase

Adding new phase to roadmap...

> Phase name?
Email Notifications

> Phase goal?
Send email notifications for task assignments, updates, and deadlines

> Requirements (one per line, empty line to finish)?
> - Send email when task assigned
> - Send daily digest of pending tasks
> - Allow users to configure notification preferences
> - Use background job queue for async sending
>

✓ Phase 7 added to roadmap
Next: Run `gsd discuss 7` when ready
```

---

### `gsd insert-phase [N]`

Insert a new phase at position N.

**Syntax**: `gsd insert-phase [position]`

**Example**:
```bash
$ gsd insert-phase 3

Current phase 3: Authentication
This will shift Authentication → Phase 4

> New phase name?
Input Validation

> Why insert here?
Need validation before authentication to prevent injection

✓ Phases renumbered
  - Old phase 3 (Authentication) → Phase 4
  - Old phase 4 (Real-time) → Phase 5
  - New phase 3: Input Validation
```

---

### `gsd remove-phase [N]`

Remove phase N from roadmap.

**Syntax**: `gsd remove-phase [phase-number]`

**Example**:
```bash
$ gsd remove-phase 8

Phase 8: Advanced Analytics

This phase has not been started. Remove it?
> y

✓ Phase 8 removed
✓ Phases renumbered (9 → 8, 10 → 9, ...)
```

---

## Session Management

### `gsd pause`

Save state for later resumption.

**Syntax**: `gsd pause`

**Example**:
```bash
$ gsd pause

Saving current state...

> Reason for pause (optional)?
> Waiting for API keys from DevOps team

✓ State saved to STATE.md
  - Phase: 3
  - Task: 2 (in progress)
  - Blocker: Waiting for API keys
  - Timestamp: 2026-01-31 14:30

Resume later with: `gsd resume`
```

---

### `gsd resume`

Resume from paused state.

**Syntax**: `gsd resume`

**Example**:
```bash
$ gsd resume

Resuming from pause...

Last state:
- Paused: 2026-01-31 14:30 (2 hours ago)
- Phase: 3 (Authentication)
- Task: 2 of 3 (Login/logout endpoints)
- Blocker: Waiting for API keys from DevOps

Blocker status:
> Resolved, API keys received

Great! Suggested next action:
`gsd execute 3` (continue task 2)
```

---

## Utility Commands

### `gsd quick [description]`

Execute a quick ad-hoc task without full planning.

**Syntax**: `gsd quick "[description]"`

**Example**:
```bash
$ gsd quick "fix login button alignment on mobile"

Quick task: fix login button alignment on mobile

Implementing fix...
- Modified src/components/LoginButton.tsx
- Changed justify-start → justify-center
- Added responsive padding

Testing...
✓ Looks good on mobile (375px width)

[fix a3f8d1c] fix: align login button center on mobile

Quick task complete!
```

**Use when**:
- Small fixes (< 10 min)
- Typos, minor UI tweaks
- Debug logging
- Quick refactorings

**Don't use when**:
- New features
- Changes affecting multiple files
- Anything requiring tests

---

### `gsd debug [description]`

Systematic debugging mode.

**Syntax**: `gsd debug "[description]"`

**Example**:
```bash
$ gsd debug "login fails with 500 error"

Debugging: login fails with 500 error

Step 1: Reproduce
> Can you reproduce? [y/n]
y

Step 2: Gather context
- Check logs
- Check recent changes (git log -5)
- Check relevant code

Found in logs:
Error: Database connection timeout

Step 3: Hypothesis
Likely cause: Connection pool exhausted

Step 4: Fix
Increasing pool size from 20 → 50...

Step 5: Verify
> Try logging in again
Works!

[fix f8a3c1d] fix: increase database connection pool size

Debug complete!
```

---

---

## Parallel Execution Commands

### `gsd execute-all`

Execute all planned phases sequentially.

**Syntax**: `gsd execute-all [--from N] [--to M] [--background]`

**Arguments**:
- `--from N`: Start from phase N (default: 1)
- `--to M`: Stop at phase M (default: last phase)
- `--background`: Run in background, return immediately

**Example**:
```bash
$ gsd execute-all --from 2 --background

🚀 Background execution started
   Phases: 2 → 6
   Output: .gsd/execution-20260204.log

   Monitor with: gsd status --live
```

**Edge cases**:
- Phase has no PLAN → Error, run `gsd plan N` first
- Previous phase incomplete → Error, complete or skip
- Already running → Error, use `gsd status --live` to check

---

### `gsd execute-parallel [N]`

Execute phase N with parallel task execution where possible.

**Syntax**: `gsd execute-parallel [phase-number] [--max-agents N] [--resume]`

**Arguments**:
- `[phase-number]`: Required. Which phase to execute
- `--max-agents N`: Maximum concurrent agents (default: 5, max: 10)
- `--resume`: Resume from last failed task

**Process**:
1. Load all PLAN-X.md files for phase
2. Build dependency graph from `<depends>` attributes
3. Topological sort into execution groups
4. For each group:
   - If single task → Execute directly
   - If multiple independent tasks → Fan-Out to background agents
   - Wait for all agents (Fan-In)
5. Continue with dependent groups
6. Verify phase

**Example**:
```bash
$ gsd execute-parallel 2 --max-agents 3

Executing Phase 2: Content Sections

Dependency analysis:
  task-1 (Setup)
     ├─→ task-2 (Hero)
     ├─→ task-3 (Benefits)
     └─→ task-4 (Footer)
           ↓
      task-5 (Integration)

Execution plan:
  Group 1: [task-1]           Sequential
  Group 2: [task-2,3,4]       Parallel (3 agents)
  Group 3: [task-5]           Sequential

Starting execution...

Group 1 (sequential):
  ✓ task-1 complete (2m 15s)

Group 2 (parallel - 3 agents):
  ├─→ Agent 1: task-2 (Hero)
  ├─→ Agent 2: task-3 (Benefits)
  └─→ Agent 3: task-4 (Footer)

  Waiting for agents...
  ✓ Agent 2: task-3 complete (2m 30s)
  ✓ Agent 3: task-4 complete (2m 45s)
  ✓ Agent 1: task-2 complete (3m 10s)

Group 3 (sequential):
  ✓ task-5 complete (1m 45s)

Phase 2 complete!
  Time: 9m 45s
  Sequential estimate: ~13m
  Saved: ~25%
```

**Edge cases**:
- Tasks have no `id` attribute → Run sequentially (safe default)
- Circular dependency detected → Error, show cycle
- Agent timeout → Retry once, then fail phase
- Max agents exceeded → Batch execution

---

### `gsd execute-overnight`

Full autopilot mode for unattended execution.

**Syntax**: `gsd execute-overnight [--from N] [--parallel]`

**Arguments**:
- `--from N`: Start from phase N (default: current phase)
- `--parallel`: Enable parallel execution where possible

**Prerequisites**:
- All phases must have PLAN files
- No pending `gsd discuss` decisions
- Git working directory clean (or auto-stash)

**Example**:
```bash
$ gsd execute-overnight --from 2 --parallel

Pre-flight checks:
  ✓ Phase 2: 4 tasks planned
  ✓ Phase 3: 3 tasks planned
  ✓ Phase 4: 3 tasks planned
  ✓ Phase 5: 3 tasks planned
  ✓ Phase 6: 2 tasks planned
  ✓ Git working directory clean
  ✓ All permissions pre-approved

🌙 Overnight Execution Started
════════════════════════════════════════

Project: Instagram Landing Page
Phases: 2 → 6 (5 phases, 15 tasks)
Mode: Parallel enabled
Started: 2026-02-04 23:00

Output: .gsd/overnight-20260204-2300.log

Monitor:
  • gsd status --live
  • tail -f .gsd/overnight-20260204-2300.log

Good night! 🌟
```

**Log format** (`.gsd/overnight-*.log`):
```
[2026-02-04 23:00:00] Starting overnight execution
[2026-02-04 23:00:01] Phase 2: Content Sections - STARTING
[2026-02-04 23:00:02]   Task 1/4: Setup - RUNNING
[2026-02-04 23:02:15]   Task 1/4: Setup - COMPLETE (2m 13s)
[2026-02-04 23:02:16]   Tasks 2-4: Parallel execution (3 agents)
[2026-02-04 23:02:16]     Agent 1: Hero - RUNNING
[2026-02-04 23:02:16]     Agent 2: Benefits - RUNNING
[2026-02-04 23:02:16]     Agent 3: Footer - RUNNING
...
[2026-02-05 02:45:00] All phases complete!
[2026-02-05 02:45:00] Total time: 3h 45m
```

**Edge cases**:
- Missing PLAN for any phase → Error before starting
- Phase fails → Stop, log error, save state for resume
- Network disconnect → Save state, can resume later

---

### `gsd status --live`

Live monitoring of running background agents.

**Syntax**: `gsd status --live [--interval N]`

**Arguments**:
- `--interval N`: Refresh interval in seconds (default: 5)

**Example**:
```bash
$ gsd status --live

╔══════════════════════════════════════════════════════════╗
║  GSD Live Status                                         ║
║  Project: Instagram Landing Page                         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Overall Progress: [████████░░░░░░░░] 53%               ║
║  Phases: 3/6 complete | Current: Phase 4                 ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  Phase 4: Social Proof                                   ║
║  ┌──────────────────────────────────────────────────────┐║
║  │ Task 1: Testimonials component  ✓ Complete  (2m 15s)│║
║  │ Task 2: Stats section           ⟳ Running   (1m 30s)│║
║  │ Task 3: Customer logos          ○ Pending           │║
║  └──────────────────────────────────────────────────────┘║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  Statistics                                              ║
║  ├─ Active agents: 1                                     ║
║  ├─ Tasks completed: 8/15                                ║
║  ├─ Elapsed time: 1h 45m                                 ║
║  ├─ Estimated remaining: ~1h 30m                         ║
║  └─ Errors: 0                                            ║
╚══════════════════════════════════════════════════════════╝

Last update: 23:45:30 | Refresh: 5s | Press Ctrl+C to exit
```

**Edge cases**:
- No background execution → Show regular status
- Execution complete → Show summary, offer next steps

---

### `gsd check-conflicts [N]`

Analyze PLANs for file conflicts before parallel execution.

**Syntax**: `gsd check-conflicts [phase-number] [--fix]`

**Arguments**:
- `[phase-number]`: Required. Which phase to analyze
- `--fix`: Automatically add `depends` attributes to resolve conflicts

**Process**:
1. Load all PLAN-X.md files for phase
2. Parse `<files>` element from each task
3. Build file → task mapping
4. Detect overlapping files between tasks without `depends` relationship
5. Report conflicts with recommendations
6. If `--fix`: Auto-add `depends` to create safe execution order

**Example - Clean analysis**:
```bash
$ gsd check-conflicts 2

Analyzing Phase 2 PLANs for file conflicts...

╔════════════════════════════════════════════════════════╗
║  File Conflict Analysis - Phase 2                      ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Task    │ Files                     │ Depends        ║
║  ────────┼───────────────────────────┼────────────────║
║  task-1  │ src/components/Button.tsx │ (none)         ║
║          │ src/components/Card.tsx   │                ║
║  ────────┼───────────────────────────┼────────────────║
║  task-2  │ src/sections/Hero.tsx     │ task-1         ║
║  ────────┼───────────────────────────┼────────────────║
║  task-3  │ src/sections/Footer.tsx   │ (none)         ║
║  ────────┼───────────────────────────┼────────────────║
║  task-4  │ src/app/page.tsx          │ task-2, task-3 ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  Analysis Results:                                     ║
║  ├─ Total tasks: 4                                     ║
║  ├─ Unique files: 5                                    ║
║  ├─ File overlaps: 0                                   ║
║  └─ Conflicts: 0                                       ║
║                                                        ║
║  ✓ No file conflicts detected                          ║
║  ✓ Safe for parallel execution                         ║
║                                                        ║
║  Parallelizable groups:                                ║
║    Group 1: [task-1]                                   ║
║    Group 2: [task-2, task-3]  ← Can run in parallel   ║
║    Group 3: [task-4]                                   ║
╚════════════════════════════════════════════════════════╝
```

**Example - With conflicts**:
```bash
$ gsd check-conflicts 2

╔════════════════════════════════════════════════════════╗
║  File Conflict Analysis - Phase 2                      ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  ⚠️  CONFLICT DETECTED                                 ║
║                                                        ║
║  File: src/components/index.ts                         ║
║  ├─ task-1: Creates Button, Card exports              ║
║  └─ task-3: Adds Footer export                        ║
║                                                        ║
║  Problem: Both tasks modify the same file but have    ║
║  no dependency relationship. Running in parallel       ║
║  will cause merge conflicts.                          ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  Recommendations:                                      ║
║                                                        ║
║  Option 1: Add dependency (recommended)               ║
║    Edit PLAN-3.md: <task depends="task-1">            ║
║                                                        ║
║  Option 2: Split shared file to separate task         ║
║    Create task-5 for index.ts, depends on all        ║
║                                                        ║
║  Option 3: Auto-fix                                   ║
║    Run: gsd check-conflicts 2 --fix                   ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Auto-fix mode**:
```bash
$ gsd check-conflicts 2 --fix

Analyzing Phase 2 PLANs for file conflicts...

⚠️  Conflict found:
    File: src/components/index.ts
    Tasks: task-1, task-3

Resolving conflict...
  Strategy: Add dependency (task-3 depends on task-1)
  Reason: task-1 creates initial exports, task-3 adds more

Updating PLAN-3.md...
  Before: <task type="auto" id="task-3">
  After:  <task type="auto" id="task-3" depends="task-1">

✓ PLAN-3.md updated

Re-analyzing...

╔════════════════════════════════════════════════════════╗
║  ✓ All conflicts resolved                              ║
║  ✓ Phase 2 is now safe for parallel execution          ║
║                                                        ║
║  New execution order:                                  ║
║    Group 1: [task-1]                                   ║
║    Group 2: [task-2, task-3]  ← Still parallel!       ║
║    Group 3: [task-4]                                   ║
╚════════════════════════════════════════════════════════╝
```

**Auto-run behavior**:
This check runs automatically before:
- `gsd execute-parallel [N]`
- `gsd execute-overnight --parallel`

If conflicts detected, execution stops with recommendations.

**Edge cases**:
- Phase has no PLANs → Error, run `gsd plan N` first
- Tasks missing `id` attribute → Warning, suggest adding IDs
- Circular dependency after fix → Error, manual resolution needed
- All tasks share one file → Suggest sequential execution

---

## Flags Reference

| Flag | Applies To | Effect |
|------|------------|--------|
| `--skip-research` | `gsd plan` | Skip research subagent even for complex topics |
| `--skip-verify` | `gsd execute` | Skip post-task self-verification (not recommended) |
| `--parallel` | `gsd execute` | Run independent tasks concurrently |
| `--force` | `gsd complete` | Complete phase even if verification failed |
| `--from N` | `gsd execute-all`, `gsd execute-overnight` | Start from phase N |
| `--to M` | `gsd execute-all` | Stop at phase M |
| `--background` | `gsd execute-all` | Run in background |
| `--max-agents N` | `gsd execute-parallel` | Max concurrent agents (default: 5) |
| `--resume` | `gsd execute-parallel` | Resume from failed task |
| `--interval N` | `gsd status --live` | Refresh interval in seconds |
| `--fix` | `gsd check-conflicts` | Auto-add dependencies to resolve conflicts |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | No .gsd/ folder (run `gsd init`) |
| 3 | Verification failed |
| 4 | Git error (uncommitted changes, etc.) |
| 5 | Invalid phase number |

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `GSD_PLANNING_DEPTH` | Override planning depth (quick/standard/comprehensive/adaptive) | `adaptive` |
| `GSD_AUTO_COMMIT` | Auto-commit after each task | `true` |
| `GSD_VERIFY_LEVEL` | Verification level (auto/manual/both/minimal) | `both` |

**Example**:
```bash
export GSD_PLANNING_DEPTH=quick
gsd plan 1  # Uses quick planning depth
```

---

## Keyboard Shortcuts (in interactive mode)

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Cancel current operation |
| Ctrl+D | Exit GSD |
| Ctrl+S | Save and pause |
| ↑/↓ | Navigate command history |

---

## Common Workflows

### Starting a new project
```bash
gsd init
gsd discuss 1
gsd plan 1
gsd execute 1
gsd verify 1
gsd complete 1
```

### Continuing from pause
```bash
gsd resume
gsd execute [N]
```

### Quick fix
```bash
gsd quick "fix typo in README"
```

### Adding a phase mid-project
```bash
gsd add-phase
gsd discuss [N]
gsd plan [N]
```

---

## Troubleshooting

### "No .gsd/ folder found"
**Solution**: Run `gsd init` to initialize the project.

### "Verification failed"
**Solution**: Check which task failed, re-execute that task.

### "Git working directory dirty"
**Solution**: Commit or stash changes before running GSD commands.

### "Phase already completed"
**Solution**: Check `gsd status` to see current phase.

### "Context too large"
**Solution**: Check file sizes, refactor if needed (see CONTEXT-ENGINEERING.md).
