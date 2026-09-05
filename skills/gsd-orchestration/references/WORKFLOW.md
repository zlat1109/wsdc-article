# GSD Workflow Details

## The Discuss-Plan-Execute-Verify Loop

### Why This Order Matters

1. **Discuss** captures YOUR vision before AI makes assumptions
2. **Plan** creates precise specifications BEFORE any code
3. **Execute** implements with fresh context per task
4. **Verify** confirms it works as YOU expected

Missing any step leads to:
- Skipping discuss → Wrong features built
- Skipping plan → Context rot, incomplete implementation
- Skipping execute discipline → Quality degradation
- Skipping verify → Broken code shipped

---

## Discuss Phase Deep Dive

The discuss phase is WHERE 80% OF BUGS ARE PREVENTED.

### Bad Approach
Skip discuss, go straight to plan. Result: Claude makes assumptions, builds wrong thing.

### Good Approach
Thorough discuss with decisions documented. Result: Plan matches your vision, execution is smooth.

### Questions to Ask During Discuss

Based on phase type:

**Visual/UI Features**:
- "What happens when [edge case]?"
- "Should this [behavior] or [alternative]?"
- "What's the priority: speed/quality/flexibility?"
- "How dense should the information be?"
- "What interactions should be supported?"

**APIs/Backend**:
- "What's the response format?"
- "How should errors be handled?"
- "What's the authentication approach?"
- "What are the rate limits?"
- "How should we version this?"

**Data/Database**:
- "What's the schema?"
- "What validation is needed?"
- "How do we handle edge cases (null, empty, huge values)?"
- "What's the migration strategy?"
- "What indexes are needed?"

**CLI Tools**:
- "What arguments/flags?"
- "What's the output format?"
- "How should errors be displayed?"
- "Interactive or batch mode?"
- "How to handle stdin/stdout/stderr?"

**AI Agent Systems** (New!):
- Automatically detected via LLM reasoning
- Offers agent-architect integration
- See "AI Agent Phase Workflow" section below

### CONTEXT.md Structure

The output of discuss should always create CONTEXT.md with:

```markdown
# Phase [N] Context

## Decisions
- **UI Layout**: Grid layout, 3 columns - Matches existing dashboard pattern
- **Error Handling**: Show toast notifications - User familiar with this UX
- **Validation**: Client and server side - Security requirement

## Out of Scope
- Advanced filtering - Defer to Phase 4
- Export to PDF - Not in v1.0 requirements

## Edge Cases
- Empty data → Show "No items yet" placeholder with CTA
- API timeout → Retry 3x with exponential backoff, then error
- Concurrent edits → Last write wins (for v1.0)

## Open Questions
- Should we add loading skeletons or spinners? → Decide during planning
```

This becomes the source of truth for planning.

---

## Plan Phase Deep Dive

Each plan is **executable, not descriptive**.

### Bad Plan
```
Create user authentication
```

Problems:
- No specifics on implementation
- No libraries mentioned
- No edge cases
- Can't be executed by another Claude instance

### Good Plan

```xml
<task type="auto">
  <name>Create login endpoint</name>
  <files>src/api/auth/login.ts</files>
  <action>
    Use jose for JWT (not jsonwebtoken - CommonJS issues with Next.js).
    Validate email/password against users table.
    Return httpOnly cookie on success (cookie name: "auth_token").
    Hash check using bcrypt.compare.

    Error cases:
    - Invalid email format → 400
    - User not found → 401 "Invalid credentials"
    - Wrong password → 401 "Invalid credentials"
    - Rate limit exceeded → 429
  </action>
  <verify>
    curl -X POST http://localhost:3000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"test@example.com","password":"password123"}'
  </verify>
  <expected>
    200 + Set-Cookie header with auth_token
    Body: {"success": true, "user": {"id": "...", "email": "..."}}
  </expected>
</task>
```

### Planning Depth: Adaptive

Adjust based on complexity:

**Simple task** (Quick):
- Minimal XML, basic acceptance criteria
- Assumes familiarity with patterns

**Medium task** (Standard):
- Clear action steps
- Edge cases mentioned
- Libraries specified

**Complex task** (Comprehensive):
- Detailed implementation guide
- All edge cases with handling
- Examples and patterns
- Common pitfalls noted

### Research Phase (Optional)

Before planning complex/unfamiliar features, spawn a research subagent:

```
Researcher context:
- Tech stack from PROJECT.md
- Phase goal from ROADMAP.md
- Specific question: "Best practice for [X] in [tech stack]"

Researcher output:
- Recommended approach
- Libraries/tools to use
- Common pitfalls
- Example code snippets

Save to: .gsd/phases/phase-N/RESEARCH.md
```

Then reference RESEARCH.md during planning.

---

## Execute Phase Deep Dive

### The Fresh Context Rule

**Before each task**:
1. **Clear mental model** of previous task
2. **Load ONLY**:
   - PROJECT.md (tech stack section ~50 lines)
   - Current PLAN-X.md (full ~150 lines)
   - Relevant source files (only those being modified)
3. **Execute** plan exactly as written
4. **Commit** immediately after completion
5. **Announce completion** with summary
6. **Clear context** (mental reset)

**Why this works**:
- No context accumulation = no quality degradation
- Each task gets full 200K token budget
- Mistakes are isolated to single commits
- Git bisect can find exact failing change

### Between Tasks

Output this EXACT format:

```
---
✓ Task 1 complete: [one-line summary]

Clearing context for Task 2...

Loading fresh context:
- PROJECT.md (tech stack section)
- PLAN-2.md (full)
- src/components/UserProfile.tsx (file being modified)

Starting Task 2: Add profile edit functionality
---
```

This announcement serves as:
1. A signal to the user about progress
2. A mental cue to Claude to actually reset
3. Documentation of what context is loaded

### Self-Verification

After implementing each task, verify against acceptance criteria in PLAN-X.md:

```
Task acceptance criteria:
- [ ] Login endpoint returns 200 on success
- [ ] httpOnly cookie is set
- [ ] Invalid credentials return 401
- [ ] Rate limiting works (429 after 5 attempts)

Self-check:
✓ Tested with curl, got 200 + Set-Cookie
✓ Cookie has httpOnly flag
✓ Wrong password gives 401
✓ Rate limiter middleware in place
```

If all criteria met → commit. If not → fix before committing.

### Commit Format

```bash
git add -A && git commit -m "feat(phase-3): add user login endpoint

- Implement POST /api/auth/login
- Use jose for JWT generation
- Add rate limiting (5 attempts/min)
- Set httpOnly auth cookie

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code restructuring, no behavior change
- `test`: Adding tests
- `chore`: Maintenance (deps, config, etc.)

---

## Verify Phase Deep Dive

Verification is NOT optional.

### Automated Checks (Always Run)

Based on tech stack and configuration:

**Python projects**:
```bash
pytest tests/ -v                    # Unit tests
pytest tests/integration/ -v        # Integration tests
mypy src/                           # Type checking
ruff check src/                     # Linting
```

**JavaScript/TypeScript**:
```bash
npm test                            # Jest/Vitest tests
npm run type-check                  # TypeScript
npm run lint                        # ESLint
npm run build                       # Build check
```

**Go**:
```bash
go test ./...                       # All tests
go vet ./...                        # Static analysis
golangci-lint run                   # Linting
```

### Manual Checks (You Do These)

Provide specific instructions:

```markdown
### Manual Verification

1. **Test login flow**:
   - Navigate to http://localhost:3000/login
   - Enter email: test@example.com, password: password123
   - Click "Log In"
   - Expected: Redirect to /dashboard, see user name in header

2. **Test invalid credentials**:
   - Use wrong password
   - Expected: Red error message "Invalid credentials"
   - No redirect

3. **Test edge cases**:
   - Empty email → Show "Email required"
   - Invalid email format → Show "Invalid email"
   - Network error → Show "Connection failed, try again"
```

### Verification Output

```
## Verification Results: Phase 3

### Automated Tests
✓ Unit tests: 24/24 passed
✓ Integration tests: 8/8 passed
✓ Type checking: No errors
✓ Linting: Clean
✓ Build: Successful

### Manual Checks
- [ ] Login flow with valid credentials - **Please verify**
- [ ] Invalid credentials handling - **Please verify**
- [ ] Edge cases (empty, invalid format) - **Please verify**

### Overall Status
PASS (automated) / PENDING (manual verification)

Next: Complete manual checks, then run `gsd complete 3`
```

### If Verification Fails

1. **Identify which task failed**
   - Check git log to see task commits
   - Review that task's PLAN-X.md

2. **Create fix plan**
   - Small fix? Use `gsd quick`
   - Large fix? Create new task in phase

3. **Re-execute**
   - Fix the specific task
   - Commit with `fix(phase-N): [description]`

4. **Verify again**
   - Re-run ALL verifications
   - Ensure no regressions

---

## State Transitions

```
Phase lifecycle:

NOT STARTED
    ↓ (gsd discuss N)
DISCUSSING → CONTEXT.md created
    ↓ (gsd plan N)
PLANNING → PLAN-X.md files created
    ↓ (gsd execute N)
EXECUTING → Code written, commits made
    ↓ (gsd verify N)
VERIFYING → Tests run, results documented
    ↓ (gsd complete N)
COMPLETE → SUMMARY.md created, STATE.md updated
    ↓
(Move to Phase N+1, start with gsd discuss N+1)
```

### Pause and Resume

**Pause** (at any point):
```bash
gsd pause
```

Creates pause marker in STATE.md:
```markdown
## Pause State
**Paused at**: 2026-01-31 14:30
**Phase**: 3 - User Authentication
**Status**: Executing (Task 2 of 3 in progress)
**Context**: Working on profile edit functionality
**Blockers**: Waiting for API key for email service
```

**Resume**:
```bash
gsd resume
```

Shows pause state and suggests next action:
```
Resuming from pause...

Last state:
- Phase 3 (User Authentication)
- Executing task 2 of 3
- Blocker: Waiting for API key

Suggested action:
1. If blocker resolved: `gsd execute 3` (continue task 2)
2. If still blocked: Update STATE.md or work on different phase
```

---

## Quick Tasks (Ad-hoc)

For small fixes outside the main workflow:

```bash
gsd quick "fix login button alignment"
```

Process:
1. No full planning
2. Make the change
3. Quick verification
4. Commit as `fix: [description]`
5. Don't update phase files

Use when:
- Typo fixes
- Minor UI tweaks
- Small refactorings
- Debug logging additions

Don't use for:
- New features
- Behavior changes
- Anything affecting multiple files

---

## Best Practices Summary

1. **Never skip discuss** - It prevents wrong assumptions
2. **Keep tasks atomic** - 15 min each, no more
3. **Fresh context per task** - No carryover
4. **Commit immediately** - Don't batch commits
5. **Verify everything** - Even "obvious" changes
6. **Document decisions** - Future you will thank you
7. **Update STATE.md** - Always current
8. **One phase at a time** - Don't plan ahead too far

---

## Common Anti-Patterns

❌ **Skip to coding**
- Skipping discuss and plan
- Results in wrong features

❌ **Accumulate context**
- Not clearing between tasks
- Results in quality degradation

❌ **Batch commits**
- Commit once per phase instead of per task
- Makes debugging harder

❌ **Skip verification**
- "It looks right" without testing
- Leads to bugs in production

❌ **Huge tasks**
- Tasks taking > 30 min
- Causes context overload

❌ **Plan too far ahead**
- Planning all phases upfront
- Requirements change, wasted effort

---

## AI Agent Phase Workflow

### Detection & Integration

GSD can automatically integrate with **agent-architect** for AI agent systems.

**When**: Phase description suggests AI agents (detected via LLM reasoning, not keywords)

**Workflow Comparison**:

```
Standard Phase:
gsd discuss N
├─ Summarize goal
├─ Identify gray areas
├─ Ask questions
└─ Create CONTEXT.md

AI Agent Phase:
gsd discuss N
├─ Summarize goal
├─ [AUTO-DETECT: AI agents]
├─ AskUserQuestion: "Run agent-architect?"
│
├─ If YES:
│   ├─ Invoke: /agent-architect
│   ├─ Phase 1: Pattern (ReAct/Planner)
│   ├─ Phase 2: Agents & Tools
│   ├─ Phase 3: Orchestration
│   ├─ Phase 4: Guardrails
│   ├─ Phase 5: Approval
│   └─ Save: ARCHITECTURE.md
│
├─ Continue standard discuss
└─ Create CONTEXT.md (+ reference to ARCHITECTURE.md)
```

### Planning with Architecture

```
gsd plan N (AI phase)

Context loaded:
├─ PROJECT.md (tech stack)
├─ ROADMAP.md (phase N)
├─ CONTEXT.md (decisions)
└─ ARCHITECTURE.md ← NEW!
    ├─ Agent definitions
    ├─ Tool specifications
    └─ Orchestration pattern

Plan generation:
├─ PLAN-1.md: Implement agents
│   └─ References: ARCHITECTURE.md agent definitions
│
├─ PLAN-2.md: Implement tools
│   └─ References: ARCHITECTURE.md tool specs
│
└─ PLAN-3.md: Orchestration & integration
    └─ References: ARCHITECTURE.md orchestration pattern
```

### Execution with Fresh Context

```
gsd execute N (AI phase)

Task 1: Agents
├─ Load (fresh):
│   ├─ PROJECT.md (tech only)
│   ├─ PLAN-1.md
│   └─ ARCHITECTURE.md (agent section)
├─ Implement agents
├─ Commit
└─ CLEAR CONTEXT

Task 2: Tools
├─ Load (fresh):
│   ├─ PROJECT.md (tech only)
│   ├─ PLAN-2.md
│   └─ ARCHITECTURE.md (tools section)
├─ Implement tools
├─ Commit
└─ CLEAR CONTEXT

Task 3: Orchestration
├─ Load (fresh):
│   ├─ PROJECT.md (tech only)
│   ├─ PLAN-3.md
│   ├─ ARCHITECTURE.md (orchestration section)
│   └─ Code from tasks 1-2 (for integration)
├─ Implement orchestration
└─ Commit
```

### File Structure Example

```
.gsd/phases/phase-2/
├── CONTEXT.md
│   ## Decisions
│   - Use Claude Agent SDK
│   - Real-time monitoring via Ralph
│   See ARCHITECTURE.md for AI system design
│
├── ARCHITECTURE.md  ← From agent-architect
│   ## Agent Team
│   - Triage Agent: Classify requests
│   - KB Agent: RAG search knowledge base
│   - Escalation Agent: Hand off to human
│
│   ## Orchestration
│   - Main orchestrator routes to specialists
│   - Sequential delegation pattern
│
│   ## Tools
│   - RAG: ChromaDB with embeddings
│   - Custom: classify_intent, search_kb
│
├── PLAN-1.md
│   Task: Implement 3 agents per ARCHITECTURE.md
│   Files: agents/triage.py, agents/kb.py, agents/escalation.py
│   References ARCHITECTURE.md for system prompts
│
├── PLAN-2.md
│   Task: Implement RAG tools per ARCHITECTURE.md
│   Files: tools/rag.py, tools/custom_tools.py
│
├── PLAN-3.md
│   Task: Orchestrator integration per ARCHITECTURE.md
│   Files: main.py, orchestrator/router.py
│
└── SUMMARY.md
    AI agent system implemented with 3 specialized agents,
    RAG knowledge base, and orchestrator routing.
```

### Benefits

1. **Architectural Rigor**: agent-architect ensures proper AI design
2. **Context Engineering**: Fresh context per task prevents degradation
3. **Seamless Integration**: Architecture flows naturally into planning
4. **Quality Consistency**: Same GSD guarantees for AI projects

### Complete Example

See [references/AGENT-INTEGRATION.md](AGENT-INTEGRATION.md) for:
- Detailed detection logic
- Full workflow examples
- ARCHITECTURE.md format specification
- Multiple scenario walkthroughs

---

## Integration with Session Continuity

GSD works alongside `.context/HANDOFF.md`:

- **HANDOFF.md**: For session continuity across compacts
- **STATE.md**: For GSD workflow state

Update both:
- Before compact → Update HANDOFF.md
- After each command → Update STATE.md

They complement each other, don't conflict.
