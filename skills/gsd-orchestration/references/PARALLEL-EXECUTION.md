# Parallel Execution in GSD

## Overview

GSD supports parallel execution of phases and tasks using the **Fan-Out / Fan-In** pattern with automatic dependency detection.

```
        [Phase 1: Setup]          ← Sequential (foundation)
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
[Phase 2] [Phase 3] [Phase 4]     ← Parallel (independent)
     │         │         │
     └─────────┼─────────┘
               ▼
        [Phase 5: Polish]          ← Sequential (aggregation)
```

---

## New Commands

### `gsd execute-all`

Execute all planned phases sequentially (one after another).

**Syntax**: `gsd execute-all [--from N] [--to M] [--background]`

**Arguments**:
- `--from N`: Start from phase N (default: 1)
- `--to M`: Stop at phase M (default: last phase)
- `--background`: Run in background, return immediately

**Process**:
```
For each phase from N to M:
  1. Load phase PLANs
  2. Execute tasks sequentially
  3. Verify phase
  4. Complete phase
  5. Move to next phase
```

**Use when**:
- You want to run everything without interaction
- Phases have dependencies between them
- Overnight execution without parallelism

---

### `gsd execute-parallel [N]`

Execute phase N with parallel task execution where possible.

**Syntax**: `gsd execute-parallel [phase-number] [--max-agents N]`

**Arguments**:
- `[phase-number]`: Required. Which phase to execute
- `--max-agents N`: Maximum concurrent agents (default: 5, max: 10)

**Process**:
```
1. Load all PLAN-X.md files for phase
2. Build dependency graph from <depends> attributes
3. Identify independent task groups
4. Fan-Out: Spawn background agents for independent tasks
5. Wait for completion (Fan-In)
6. Execute dependent tasks sequentially
7. Verify and complete
```

**Example**:
```
Phase 2 tasks:
- PLAN-1: Hero Section (no deps)
- PLAN-2: Benefits Section (no deps)
- PLAN-3: Social Proof (no deps)
- PLAN-4: Integration (depends: 1,2,3)

Execution:
┌─→ Agent 1: PLAN-1 (Hero)
├─→ Agent 2: PLAN-2 (Benefits)    ← Parallel!
├─→ Agent 3: PLAN-3 (Social)
│
└─→ Wait for all...
         │
         ▼
    Agent 4: PLAN-4 (Integration)  ← Sequential
```

---

### `gsd execute-overnight`

Full autopilot mode for unattended execution.

**Syntax**: `gsd execute-overnight [--from N] [--parallel]`

**Arguments**:
- `--from N`: Start from phase N (default: current phase)
- `--parallel`: Enable parallel execution where possible

**Process**:
```
1. Validate all phases have PLANs (error if not)
2. Pre-approve all required permissions
3. Spawn master orchestrator as background agent
4. Return output file path for monitoring

Master orchestrator:
  For each phase:
    - If --parallel and tasks are independent: Fan-Out
    - Else: Sequential execution
    - Auto-verify after each phase
    - Log progress to output file
    - Continue on success, stop on failure
```

**Output file**: `.gsd/overnight-execution-{timestamp}.log`

**Example**:
```bash
$ gsd execute-overnight --from 2 --parallel

🌙 Overnight execution started
   Output: .gsd/overnight-execution-20260204-2300.log

   Monitor progress:
   - tail -f .gsd/overnight-execution-20260204-2300.log
   - gsd status --live

   Phases to execute: 2, 3, 4, 5, 6
   Estimated completion: ~4-6 hours

Good night! 🌟
```

---

### `gsd status --live`

Live monitoring of running background agents.

**Syntax**: `gsd status --live [--interval N]`

**Arguments**:
- `--interval N`: Refresh interval in seconds (default: 5)

**Output**:
```
╔══════════════════════════════════════════════════════╗
║  GSD Live Status - Instagram Landing Page            ║
╠══════════════════════════════════════════════════════╣
║  Overall: [████████░░] 80%  (4/5 phases complete)    ║
╠══════════════════════════════════════════════════════╣
║  Phase 5: Lead Form                                  ║
║  ├─ Task 1: Form component      ✓ Complete          ║
║  ├─ Task 2: Validation          ⟳ Running (2m 15s)  ║
║  └─ Task 3: Submit handler      ○ Pending           ║
╠══════════════════════════════════════════════════════╣
║  Active Agents: 1                                    ║
║  Completed Tasks: 12/15                              ║
║  Errors: 0                                           ║
╚══════════════════════════════════════════════════════╝
```

---

### `gsd check-conflicts [N]`

Analyze PLANs for file conflicts before parallel execution.

**Syntax**: `gsd check-conflicts [phase-number] [--fix]`

**Arguments**:
- `[phase-number]`: Required. Which phase to analyze
- `--fix`: Attempt to auto-resolve conflicts by adding dependencies

**Process**:
```
1. Load all PLAN-X.md files for phase
2. Extract <files> from each task
3. Build file → tasks mapping
4. Identify files touched by multiple tasks
5. Report conflicts or suggest resolution
```

**Output (no conflicts)**:
```
✓ Phase 2 conflict check passed

Files analyzed: 12
Tasks analyzed: 4
Conflicts found: 0

Safe for parallel execution!
```

**Output (conflicts found)**:
```
⚠ Phase 2 has file conflicts

Conflicts detected:
┌────────────────────────────────────────────────────┐
│ src/components/Button.tsx                          │
│   ├─ PLAN-1 (Hero Section)                         │
│   └─ PLAN-3 (CTA Section)        ← CONFLICT       │
├────────────────────────────────────────────────────┤
│ src/styles/global.css                              │
│   ├─ PLAN-1 (Hero Section)                         │
│   ├─ PLAN-2 (Benefits Section)                     │
│   └─ PLAN-4 (Footer)             ← CONFLICT       │
└────────────────────────────────────────────────────┘

Options:
1. Add dependency: PLAN-3 depends on PLAN-1
2. Split shared file into task-specific files
3. Run with --fix to auto-add dependencies

Run: gsd check-conflicts 2 --fix
```

**With --fix flag**:
```
$ gsd check-conflicts 2 --fix

Analyzing Phase 2 for conflicts...

Found 2 conflicts:
- src/components/Button.tsx: PLAN-1, PLAN-3
- src/styles/global.css: PLAN-1, PLAN-2, PLAN-4

Auto-fixing:
✓ Added: PLAN-3 depends="task-1"
✓ Added: PLAN-2 depends="task-1"
✓ Added: PLAN-4 depends="task-1,task-2"

Updated dependency graph:
  task-1 (Hero)
     │
     ├──→ task-2 (Benefits) ──→ task-4 (Footer)
     │
     └──→ task-3 (CTA)

Run gsd execute-parallel 2 to proceed.
```

**Use when**:
- Before running `gsd execute-parallel`
- After creating or modifying PLANs
- When overnight execution is planned
- To validate parallel-safe task design

---

## Dependency Detection

### Automatic Detection

GSD automatically detects dependencies from:

1. **Explicit `<depends>` attribute** in PLAN XML
2. **File references** between tasks
3. **Phase order** (phases must complete in order)

### PLAN XML with Dependencies

```xml
<task type="auto" id="task-1">
  <name>Create base components</name>
  <files>src/components/Button.tsx, src/components/Card.tsx</files>
  <outputs>Button, Card components</outputs>
  <action>...</action>
</task>

<task type="auto" id="task-2" depends="task-1">
  <name>Create Hero section</name>
  <files>src/sections/Hero.tsx</files>
  <inputs>Button, Card from task-1</inputs>
  <action>
    Use Button and Card components from task-1.
    ...
  </action>
</task>

<task type="auto" id="task-3">
  <name>Create Footer</name>
  <files>src/sections/Footer.tsx</files>
  <!-- No depends = independent, can run parallel with task-2 -->
  <action>...</action>
</task>
```

### Dependency Graph Visualization

During `gsd plan`, show dependency graph:

```
Dependency Graph for Phase 2:

task-1 (Base components)
   │
   ├──→ task-2 (Hero) ──→ task-4 (Integration)
   │                          ↑
   └──→ task-3 (Footer) ──────┘

Parallel groups:
  Group 1: [task-1]           ← Must run first
  Group 2: [task-2, task-3]   ← Can run parallel
  Group 3: [task-4]           ← Must run last
```

---

## Fan-Out / Fan-In Pattern

### How It Works

```
                    ORCHESTRATOR
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │ Agent 1 │     │ Agent 2 │     │ Agent 3 │    FAN-OUT
   │ Task A  │     │ Task B  │     │ Task C  │    (Parallel)
   └────┬────┘     └────┬────┘     └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                    ORCHESTRATOR                   FAN-IN
                    (Collect results)              (Aggregate)
                         │
                         ▼
                   ┌─────────┐
                   │ Agent 4 │                     SEQUENTIAL
                   │ Task D  │                     (Dependent)
                   └─────────┘
```

### Implementation

```python
# Pseudo-code for orchestrator logic

def execute_phase_parallel(phase_num, max_agents=5):
    plans = load_all_plans(phase_num)
    dep_graph = build_dependency_graph(plans)

    # Topological sort into execution groups
    groups = topological_sort_groups(dep_graph)

    for group in groups:
        if len(group) == 1:
            # Single task - run directly
            execute_task(group[0])
        else:
            # Multiple independent tasks - fan out
            agents = []
            for task in group[:max_agents]:
                agent = spawn_background_agent(
                    subagent_type="general-purpose",
                    prompt=build_task_prompt(task),
                    run_in_background=True
                )
                agents.append(agent)

            # Fan in - wait for all
            results = wait_for_all(agents)

            # Check for failures
            for result in results:
                if result.failed:
                    handle_failure(result)
                    return

        # Clear context before next group
        clear_context()

    # Verify phase
    verify_phase(phase_num)
```

---

## Error Handling

### Retry with Exponential Backoff

```
Attempt 1: Execute task
  └─ Failure → Wait 2 seconds

Attempt 2: Execute task
  └─ Failure → Wait 4 seconds

Attempt 3: Execute task
  └─ Failure → Mark task as FAILED, stop phase
```

### Failure Modes

| Scenario | Behavior |
|----------|----------|
| Single task fails | Stop phase, report failure, suggest fix |
| Background agent timeout | Retry once, then fail |
| Multiple parallel failures | Stop all agents, report all failures |
| Network error | Retry with backoff (max 3 attempts) |

### Recovery

```bash
# After fixing the issue
$ gsd execute-parallel 3 --resume

Resuming Phase 3 from task-2...
- task-1: ✓ Already complete
- task-2: ⟳ Retrying...
```

---

## Claude Code Constraints

### Critical Limits (Official Documentation)

| Constraint | Value | Impact |
|------------|-------|--------|
| Max concurrent agents | ~10 | Batch if more tasks |
| No nested subagents | 1 level | Orchestrator spawns, agents execute |
| **No MCP in background** | Hard limit | Use standard tools only |
| Context per agent | 200K | Keep plans < 3K tokens each |

### MCP Tools Constraint (CRITICAL)

**MCP tools are NOT available in background subagents.** This is a hard constraint from Claude Code.

What this means for GSD:
- Background agents can only use: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `Task` (foreground only)
- If a task needs MCP tools (databases, APIs, external services) → Run as **foreground** subagent
- Plan your tasks to avoid MCP dependencies in parallel execution

**Safe for background**:
- File creation/editing
- Running build/test commands
- Git operations
- Code analysis

**Requires foreground**:
- Database operations (MCP)
- External API calls (MCP)
- Cloud services (MCP)

### No Nested Subagents (CRITICAL)

**Subagents cannot spawn other subagents.** This is a hard constraint.

What this means for GSD:
- The orchestrator (main conversation) spawns all agents
- Background agents execute their task and return results
- Agents cannot delegate to other agents
- All parallelism decisions happen at the orchestrator level

### Batching for Large Phases

If phase has > 10 independent tasks:

```
Round 1: Spawn agents for tasks 1-10
Wait for completion

Round 2: Spawn agents for tasks 11-20
Wait for completion

...
```

---

## Performance Benchmarks

Based on research findings:

| Metric | Sequential | Parallel | Improvement |
|--------|------------|----------|-------------|
| 6-phase project | ~3 hours | ~1.5 hours | **50%** |
| Independent tasks | 1x | 0.64x | **36% faster** |
| Error rate | 5% | 0.11%* | **45x better** |

*With consensus voting across agents (optional feature)

---

## Best Practices

### 1. Design for Parallelism

When writing PLANs, think about independence:

```xml
<!-- GOOD: Explicit dependencies, clear boundaries -->
<task id="task-1">
  <outputs>UserService, AuthMiddleware</outputs>
</task>

<task id="task-2" depends="task-1">
  <inputs>UserService from task-1</inputs>
</task>

<!-- BAD: Implicit dependencies, unclear -->
<task>Create user stuff</task>
<task>Create more user stuff</task>
```

### 2. Keep Tasks Atomic

Each task should:
- Take 10-15 minutes
- Have clear inputs/outputs
- Be independently verifiable
- Not require context from other tasks

### 3. Pre-Plan Everything

For overnight execution:
```bash
# Day: Plan all phases
gsd discuss 1 && gsd plan 1
gsd discuss 2 && gsd plan 2
gsd discuss 3 && gsd plan 3
...

# Night: Execute all
gsd execute-overnight --parallel
```

### 4. Check for Conflicts Before Parallel Execution

**Always run `check-conflicts` before parallel execution**:

```bash
# After planning, before executing
gsd check-conflicts 2

# If conflicts found, auto-fix or manually resolve
gsd check-conflicts 2 --fix

# Then execute
gsd execute-parallel 2
```

This prevents agents from stepping on each other by ensuring:
- No two tasks modify the same file
- Dependencies are explicitly declared
- Parallel groups are safely isolated

### 5. Monitor Progress

Always use `--background` with a way to check status:

```bash
# Start overnight execution
gsd execute-overnight --parallel

# In another terminal (or next morning)
gsd status --live

# Or check log directly
tail -f .gsd/overnight-execution-*.log
```

---

## Example: Landing Page Project

### Phase Structure with Parallelism

```yaml
phases:
  phase-1:
    name: "Setup & Design System"
    tasks: [setup]
    parallel: false  # Must run first

  phase-2:
    name: "Content Sections"
    tasks: [hero, benefits, social, form]
    parallel: true   # All independent!
    depends_on: [phase-1]

  phase-3:
    name: "Polish & Integration"
    tasks: [responsive, seo, performance]
    parallel: false  # Sequential for consistency
    depends_on: [phase-2]
```

### Execution Timeline

```
Sequential (old way):
Phase 1 ──→ Phase 2 ──→ Phase 3
  30m        2h          1h
Total: 3.5 hours

Parallel (new way):
Phase 1 ──→ ┌── Hero (30m)
  30m       ├── Benefits (30m)  ← Parallel!
            ├── Social (30m)
            └── Form (30m)
                    │
                    ▼
               Phase 3
                 1h
Total: 2 hours (43% faster)
```

---

## Troubleshooting

### "Max agents reached"

**Problem**: Trying to spawn more than 10 concurrent agents.

**Solution**: GSD automatically batches. If you see this warning, it's informational only.

### "Dependency cycle detected"

**Problem**: Task A depends on B, B depends on A.

**Solution**: Review your PLAN files. Remove circular dependency or merge tasks.

### "Background agent timeout"

**Problem**: Agent didn't complete within expected time.

**Solution**:
1. Check `.gsd/overnight-execution-*.log` for errors
2. Run `gsd status` to see current state
3. Resume with `gsd execute-parallel N --resume`

### "Cannot parallelize - missing dependencies"

**Problem**: Tasks don't have explicit `<depends>` attributes.

**Solution**: Add `id` and `depends` attributes to PLAN XML, or let GSD run sequentially.

### "File conflicts detected"

**Problem**: Multiple tasks modify the same file, risking merge conflicts.

**Solution**:
1. Run `gsd check-conflicts N` to identify conflicts
2. Use `gsd check-conflicts N --fix` to auto-add dependencies
3. Or manually redesign tasks to isolate file ownership
4. Consider splitting shared files into task-specific files

---

## Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `GSD_MAX_PARALLEL_AGENTS` | Maximum concurrent agents | `5` |
| `GSD_PARALLEL_TIMEOUT` | Timeout per task (ms) | `600000` (10 min) |
| `GSD_RETRY_ATTEMPTS` | Max retry attempts | `3` |
| `GSD_RETRY_BACKOFF` | Initial backoff (ms) | `2000` |

### Project-Level Config

In `.gsd/config.yaml`:

```yaml
parallel:
  enabled: true
  max_agents: 5
  timeout_per_task: 600000
  retry:
    attempts: 3
    backoff_multiplier: 2

overnight:
  auto_verify: true
  stop_on_failure: true
  notify_on_complete: false  # Future: Slack/email notification
```
