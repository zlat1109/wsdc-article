---
name: discovery-interview
description: Run a structured product discovery interview that turns vague ideas into a concrete, testable plan. Use when the user asks to clarify a product idea, validate a problem, prepare customer interviews, or define research goals before implementation.
---

# Discovery Interview

Use this skill to move from fuzzy requests to clear discovery outputs.

## Outcomes

Produce one or more of:
- Discovery brief (problem, goals, constraints, assumptions)
- Interview plan (segment, method, script, logistics)
- Decision-ready synthesis (key risks, next experiments, success criteria)

## Interview Principles

- Ask about **past behavior**, not hypothetical intent (Mom Test style).
- Keep questions neutral; avoid leading language.
- Prefer 1 question at a time; adapt based on answers.
- Explicitly surface uncertainty, conflicts, and assumptions.
- Do not jump to solutioning until problem evidence is clear.

## Process (Phased)

### Phase 1: Orientation (2-3 questions)

Collect:
1. What problem area the user wants to understand.
2. Why now (trigger / urgency).
3. What decision this discovery should inform.

### Phase 2: Discovery Core (adaptive deep dive)

Cover relevant categories with 2-4 questions each:

1. **Problem & Goals**
   - Problem statement, success metrics, non-goals.
2. **Target Segment**
   - Primary users/customers, access constraints, sample quality.
3. **Current Behavior**
   - Current workflow, alternatives, workarounds, frequency.
4. **Constraints**
   - Timeline, team, budget, legal/compliance, tooling limits.
5. **Decision Context**
   - What decision will be made after interviews and by whom.

### Phase 3: Method Selection

Recommend the best method based on context:
- Problem validation interviews
- Jobs-to-be-Done interviews
- Churn/retention interviews
- Feature prioritization interviews

For each recommendation, state:
- Why it fits
- Risks/biases to watch
- Minimum sample target

### Phase 4: Conflict & Gap Resolution

If conflicts appear (e.g., "quick" + "high confidence"), force prioritization:
- Which tradeoff is acceptable?
- What evidence threshold is required for the decision?

If knowledge gaps remain:
- Call out exactly what is unknown.
- Propose the smallest next research step to close it.

### Phase 5: Completeness Check

Before final output, verify:
- Research goal is explicit.
- Segment and access are realistic.
- Method and script align with goal.
- Success criteria are measurable.
- Next decision owner and date are defined.

## Output Template

Use this structure in final output.

### 1) Discovery Brief
- Problem:
- Goal:
- Decision to make:
- Constraints:
- Critical assumptions:

### 2) Interview Plan
- Segment:
- Recruiting approach:
- Method:
- Number of interviews:
- Timeline:

### 3) Interview Script (30-40 min)
- Warm-up (5 min)
- Context and current behavior (10 min)
- Deep problem exploration (15 min)
- Priority and impact (5 min)
- Wrap-up (3-5 min)

### 4) Bias Guardrails
- Leading questions to avoid:
- Confirmation bias risks:
- Evidence quality checks:

### 5) Success Criteria
- What would confirm the problem?
- What would falsify the hypothesis?
- What action follows each outcome?

## Interaction Rules

- Ask concise, numbered questions.
- If the user is busy, offer a "fast track" (max 4 questions).
- If the user asks for depth, continue full phased mode.
- At each phase boundary, summarize in 3-5 bullets.
- Keep artifacts directly usable by PM/analyst/stakeholder teams.

## Fast Track Mode (when user asks for speed)

Ask only:
1. What decision are we trying to make?
2. Which user segment matters most right now?
3. What constraint is hardest (time/access/budget)?
4. Which risk worries you most if we are wrong?

Then produce:
- lean interview plan,
- 8-10 core questions,
- one-week execution checklist.
