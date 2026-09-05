# Context Engineering Principles

## The Problem: Context Rot

As Claude fills its context window, quality degrades:

### How Context Degradation Happens

1. **Early conversation** (5K tokens):
   - Full attention to each task
   - Detailed responses
   - Careful verification

2. **Mid conversation** (50K tokens):
   - Starting to summarize
   - "I'll be more concise now"
   - Skipping some details

3. **Late conversation** (150K+ tokens):
   - Cutting corners
   - "Continuing from before..." (assumes you remember)
   - Missing edge cases
   - Incomplete verification

### Why This Happens

- **Attention mechanism**: Early tokens weighted heavily, recent tokens matter less
- **Recency bias**: Focuses on latest messages, loses early context
- **Compression**: To fit more context, Claude mentally compresses earlier information
- **Fatigue analog**: Not actual fatigue, but similar quality degradation pattern

### Real-World Impact

Without context engineering:
- **Hour 1**: Perfect code
- **Hour 2**: Good code with minor issues
- **Hour 3**: Bugs introduced, tests skipped
- **Hour 4**: Major regressions, incomplete features

With context engineering (GSD):
- **Hour 1-10+**: Consistent quality because each task starts fresh

---

## The Solution: Fresh Context Per Task

Each task starts with empty context, loads only:
1. Tech stack (~50 lines from PROJECT.md)
2. Current task plan (~150 lines from PLAN-X.md)
3. Relevant source files (~500-2000 lines)

**Total per task**: ~700-2200 tokens
**Available**: 200,000 tokens
**Utilization**: ~1% of capacity
**Result**: No degradation possible

### Comparison

**Without GSD** (traditional approach):
```
Task 1:  2K context   | Quality: ★★★★★
Task 2: 10K context   | Quality: ★★★★☆
Task 3: 30K context   | Quality: ★★★☆☆
Task 4: 80K context   | Quality: ★★☆☆☆
Task 5: 150K context  | Quality: ★☆☆☆☆
```

**With GSD** (fresh context):
```
Task 1: 1K context    | Quality: ★★★★★
Task 2: 1K context    | Quality: ★★★★★
Task 3: 1.5K context  | Quality: ★★★★★
Task 4: 1.2K context  | Quality: ★★★★★
Task 5: 1K context    | Quality: ★★★★★
```

---

## What To Load When

### During `gsd init`
**Load**: Nothing (fresh start)

**Why**: No prior context needed. User answers questions, we generate files.

---

### During `gsd discuss`
**Load**:
- PROJECT.md (full) ~300 lines
- ROADMAP.md (current phase only) ~50 lines
- STATE.md (decisions section) ~30 lines

**Total**: ~380 lines (~500 tokens)

**Why**:
- PROJECT.md: Understand project vision and constraints
- ROADMAP.md: Know phase requirements
- STATE.md: Aware of previous decisions

**Don't load**:
- Other phases from ROADMAP.md (not relevant yet)
- Old phase SUMMARY.md files (discuss is forward-looking)
- Code files (discuss phase = no code)

---

### During `gsd plan`
**Load**:
- PROJECT.md (tech stack section only) ~50 lines
- ROADMAP.md (current phase only) ~50 lines
- CONTEXT.md (if exists from discuss) ~100 lines
- Previous phase SUMMARY.md (if exists) ~80 lines

**Total**: ~280 lines (~400 tokens)

**Why**:
- Tech stack: Know what tools to use
- Phase requirements: What to build
- CONTEXT.md: Decisions made in discuss
- Previous SUMMARY: What's already built

**Don't load**:
- Full PROJECT.md (vision not needed for planning)
- Other phases (not relevant)
- Code files (planning, not implementing)
- REQUIREMENTS.md (too broad, phase requirements sufficient)

**Optional: Research subagent**

If spawning researcher:
```
Researcher context:
- Tech stack from PROJECT.md (50 lines)
- Specific question (e.g., "Best state management for Next.js")

Researcher outputs to: RESEARCH.md
Then planner loads RESEARCH.md (~200 lines)
```

---

### During `gsd execute` (per task)
**Load** (fresh for EACH task):
- PROJECT.md (tech stack section only) ~50 lines
- Current PLAN-X.md (full) ~150 lines
- Relevant source files (only those being modified) ~500-2000 lines

**Total**: ~700-2200 lines (~1000-3000 tokens)

**Why**:
- Tech stack: Know conventions, libraries
- PLAN-X.md: Full implementation spec
- Source files: Understand existing code

**Don't load**:
- Previous task's PLAN (not relevant)
- Other source files (not being modified)
- Full PROJECT.md (vision not needed during execution)
- REQUIREMENTS.md (plan already has requirements)
- STATE.md (not needed for task execution)

**CRITICAL**: Clear context between tasks!

```
Task 1 context:
- PROJECT.md (tech)
- PLAN-1.md
- src/api/login.ts

[Execute Task 1]
[Commit]

**CLEAR ALL CONTEXT**

Task 2 context:
- PROJECT.md (tech)  ← Reload fresh!
- PLAN-2.md
- src/components/LoginForm.tsx

[Execute Task 2]
...
```

---

### During `gsd verify`
**Load**:
- ROADMAP.md (phase goals) ~50 lines
- All PLAN-X.md for current phase ~450 lines (3 plans × 150 each)
- STATE.md ~100 lines

**Total**: ~600 lines (~800 tokens)

**Why**:
- Phase goals: What we're verifying against
- All PLANs: All acceptance criteria
- STATE.md: Document results here

**Don't load**:
- Code files (verification runs commands, doesn't read code)
- PROJECT.md (not needed for verification)
- Other phases (verifying current only)

---

### During `gsd complete`
**Load**:
- ROADMAP.md (to update) ~400 lines
- STATE.md (to update) ~100 lines
- All PLAN-X.md (to summarize) ~450 lines

**Total**: ~950 lines (~1300 tokens)

**Why**:
- Need to update these files
- Summarize what was built

---

### During `gsd status`
**Load**:
- STATE.md only ~100 lines

**Total**: ~100 lines (~150 tokens)

**Why**: STATUS reads from STATE, that's all it needs.

---

## Size Limits

Keep files within these limits to prevent context bloat:

| File | Target Lines | Max Lines | Why |
|------|--------------|-----------|-----|
| PROJECT.md | 200-300 | 500 | Loaded frequently, must stay lean |
| REQUIREMENTS.md | 500-800 | 1000 | Reference only, rarely loaded |
| ROADMAP.md | 300-400 | 500 | Loaded often, one section at a time |
| STATE.md | 100-150 | 200 | Loaded often, should be current state only |
| PLAN-X.md | 100-150 | 200 | Loaded fully during execute, must be concise |
| CONTEXT.md | 150-200 | 300 | Loaded during plan, should capture decisions |
| RESEARCH.md | 500-1000 | 1000 | Loaded during plan if complex topic |
| SUMMARY.md | 50-100 | 150 | Loaded during next phase plan |

### What To Do When Files Exceed Limits

**PROJECT.md too large**:
- Move detailed requirements to REQUIREMENTS.md
- Move architecture diagrams to separate docs
- Keep only: vision, problem, tech stack, success criteria

**ROADMAP.md too large**:
- Each phase should be ~30-50 lines
- If > 500 lines total, you have too many phases
- Consider grouping related features

**STATE.md too large**:
- Archive old decisions to ARCHIVE.md
- Keep only current phase info
- Remove completed phases (they're in SUMMARY.md)

**PLAN-X.md too large**:
- Task is too complex, split it
- Each task = ~15 min of work
- If can't fit spec in 200 lines, it's multiple tasks

---

## Anti-Patterns

### ❌ Loading All .gsd/ Files At Once

**Bad**:
```
Before executing task, load:
- PROJECT.md
- REQUIREMENTS.md
- ROADMAP.md
- STATE.md
- All PLAN files
- All SUMMARY files
```

**Why bad**: 3000+ lines of context, only need 200.

**Good**:
```
Before executing task 2, load:
- PROJECT.md (tech section only)
- PLAN-2.md
- src/components/LoginForm.tsx
```

---

### ❌ Keeping Previous Task Context

**Bad**:
```
Task 1: Load PLAN-1.md, execute, commit
Task 2: Keep PLAN-1.md in mind, load PLAN-2.md, execute
```

**Why bad**: Context accumulates, quality degrades.

**Good**:
```
Task 1: Load PLAN-1.md, execute, commit, **CLEAR**
Task 2: Load PLAN-2.md (fresh!), execute, commit, **CLEAR**
```

---

### ❌ Plans With 5+ Tasks

**Bad**:
```
Phase 3: User authentication
- Task 1: Database schema
- Task 2: Login endpoint
- Task 3: Logout endpoint
- Task 4: Password reset
- Task 5: Email verification
- Task 6: Login UI
- Task 7: Tests
```

**Why bad**: Executor must track 7 tasks, complex dependencies.

**Good**:
```
Phase 3: Core authentication
- Task 1: Database + login endpoint
- Task 2: Login UI + verification
- Task 3: Password reset flow

Phase 4: Enhanced auth
- Task 1: Email verification
- Task 2: 2FA support
```

---

### ❌ Huge PROJECT.md With Examples

**Bad**:
```markdown
## Tech Stack
- Next.js 14

Example code:
[500 lines of example Next.js code]

## Database
- PostgreSQL

Example schema:
[300 lines of schema examples]
```

**Why bad**: PROJECT.md loaded in many commands, 800 lines is too much.

**Good**:
```markdown
## Tech Stack
- Next.js 14 (App Router)
- PostgreSQL 15
- Drizzle ORM
- Tailwind CSS

See examples/ folder for code samples.
```

---

## Patterns

### ✅ Load Minimum Necessary

Each command has precise context needs:
- `discuss`: Vision + requirements
- `plan`: Tech + phase requirements + decisions
- `execute`: Tech + task spec + relevant code
- `verify`: Goals + all task specs
- `complete`: Files to update + task summaries

Never load "just in case".

---

### ✅ Clear Context Between Tasks

Announce context clearing:
```
✓ Task 1 complete

Clearing context for Task 2...

Loading fresh context:
- PROJECT.md (tech stack)
- PLAN-2.md
- src/components/Dashboard.tsx

Starting Task 2: Implement dashboard layout
```

This is not just messaging - it's a real mental reset.

---

### ✅ 2-3 Tasks Per Plan

Sweet spot for atomic execution:
- **1 task**: Maybe too large, consider splitting
- **2-3 tasks**: Perfect balance
- **4+ tasks**: Definitely split into multiple phases

---

### ✅ Concise PROJECT.md, Details In References

**PROJECT.md** (always loaded):
```markdown
## Tech Stack
- Python 3.11+
- FastAPI
- PostgreSQL
- Redis
```

**References** (loaded on demand):
```markdown
references/architecture.md - System design
references/api-spec.md - Full API documentation
references/database.md - Schema details
```

---

## Verification of Context Engineering

How to check if GSD is working correctly:

### Check 1: Task Context Size
After each `gsd execute` task, context should be < 3000 tokens.

Monitor with:
```
"Loading fresh context:
- PROJECT.md (tech): ~50 lines
- PLAN-2.md: ~150 lines
- src/file.ts: ~800 lines
Total: ~1000 lines"
```

If > 5000 tokens, something is wrong.

### Check 2: Quality Consistency
Task 1 quality = Task 10 quality.

Signs of degradation:
- Later tasks skip tests
- Comments like "continuing from before"
- Assumptions about earlier code
- Incomplete verification

If this happens, context wasn't cleared properly.

### Check 3: File Size Growth
PROJECT.md should not grow beyond 500 lines.

If it does:
- Requirements crept in → Move to REQUIREMENTS.md
- Examples added → Remove or move to references/
- Multiple decisions → Move to CONTEXT.md for phases

---

## Advanced: Subagent Context Engineering

When spawning subagents (researcher, planner, executor):

### Researcher Subagent
**Input context**: Query + tech stack (100 lines)
**Output**: RESEARCH.md (max 1000 lines)
**Why**: Focused research, bounded output

### Planner Subagent
**Input context**: Phase goal + CONTEXT.md + tech stack (200 lines)
**Output**: PLAN-X.md files (max 200 each)
**Why**: Creates atomic task plans

### Checker Subagent
**Input context**: PLAN-X.md + requirements (300 lines)
**Output**: Validation report or approval
**Why**: Validates plan completeness

### Executor Subagent
**Input context**: Single PLAN-X.md + relevant files (1000-2000 lines)
**Output**: Code implementation
**Why**: Executes one task with fresh context

Each subagent operates independently with minimal context.

---

## Summary: Context Engineering Rules

1. **Load only what you need** for current command
2. **Clear context between tasks** - announce it explicitly
3. **Keep files within size limits** - refactor if needed
4. **Never load "just in case"** - be precise
5. **Subagents get minimal context** - focused inputs
6. **Monitor context size** - if > 5K tokens, investigate
7. **Quality should be consistent** - task 1 = task 10

These rules are what makes GSD reliable for long-term solo development.
