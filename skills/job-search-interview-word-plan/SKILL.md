---
name: job-search-interview-word-plan
description: Builds English interview prep with Word Plans (starter phrases for live calls) and optional full scripts (rehearsal). Mines JD pain points, CAR/STAR skeletons, Yes+justification, and Just to lines. Use for recruiter/technical interviews, interview HTML cheatsheets, Word Plan, english30sec, or non-native English interview prep.
---

# Job Search Interview — Word Plan + Scripts (EN)

Adapted from english30sec methodology, with a **dual-mode** default for Denis:

| Mode | Purpose | On the call |
|------|---------|-------------|
| **Word Plan** | Starters + CAR bullets | ✅ Primary — glance, then speak |
| **Full script** | Rehearsal paragraphs | ❌ Do not read verbatim (unless user explicitly chooses to) |

Integrates with `projects/job-search/` career OS. Facts only from `career/PROFILE.md`, `career/source-of-truth/storytellings.md`, and the tailored CV.

## When to use

- Interview prep for any application in `applications/<slug>/`
- User asks for cheatsheet / HTML prep
- After `interview-prep-generator` (scripts) or instead of script-only output

## Default output mode: **dual**

Unless user says `word plan only`:

1. **`<slug>_word_plan.html`** — call sheet (starters, pains, Yes/No, Just to)
2. **`<slug>_interview_scripts.html`** — full paragraphs for **rehearsal** (same questions, richer wording)

Link both from the application hub. Label scripts clearly: *Rehearsal — build muscle memory, then switch to Word Plan on the call.*

If user says `scripts only`, still add a minimal Word Plan section at the top (at least intro + 2 CAR starters per story).

## Anti-patterns

| Avoid | Why |
|-------|-----|
| Scripts **without** Word Plan | No lightweight fallback under stress |
| Word Plan **without** any rehearsal path | Harder to internalize phrasing first time |
| School outline only (Intro / Body / Conclusion) | Ideas yes, English formulations no |
| Self-focused intro ignoring JD | Fit to employer pains matters more |
| Bare "Yes" / "No" | EN expects Yes/No + one sentence |
| Invented impact metrics | PROFILE numbers only |

## Workflow

### 1. JD pain mining

Read the JD (Lever/Greenhouse text or URL). Extract **phrases → likely pain → your evidence**.

Common BI/DA mappings:

| JD signal | Likely need | Map to (examples) |
|-----------|-------------|-------------------|
| results-driven / metrics-focused | Proof of impact | Confirmed metrics from PROFILE |
| cross-functional / stakeholders | Communication | Discovery sessions, Notion docs |
| self-starter / independent | Low hand-holding | End-to-end BI ownership, remote |
| SQL / columnar / Tableau | Core stack | ClickHouse, 50+ sources, etc. |
| methodical troubleshooting | Structured problem-solving | CAR story: slow dashboards → DB fix |

Output: table in `reference.md` format → section **JD pains** in deliverable.

### 2. Self-intro (employer-fit, not resume recitation)

Build **60–90 sec** from **2–3 JD pains**, not "I am a BI analyst with 4 years…" only.

Word Plan starters (pick 3–4):

- `What caught my attention in this role is…`
- `In my current role, I'm responsible for…`
- `That connects to what you need around…`

Anchor numbers on paper only (e.g. `50+ sources`, `4+ years`) — not full sentences.

### 3. Word Plan per expected question

For each of **3–4 likely questions**, list **4–6 starter phrases** (not answers):

```
Q: Tell me about yourself
→ In my current role, I…
→ One area I own is…
→ What matters for this role is…
```

Include gaps honestly with starters:

- `I want to be transparent: …`
- `My production experience is mostly …, but …`

Full phrase bank: [reference.md](reference.md).

### 4. CAR stories (2 max)

From `storytellings.md`. **Bullet skeleton only:**

- **Challenge:** (one line)
- **Action:** (2–3 bullets)
- **Result:** (metrics from PROFILE)

Label CAR explicitly (same as STAR; teacher uses CAR).

### 5. Yes / No + justification

For recruiter screen, pre-write **short** patterns:

```
Have you used Vertica?
→ No, I haven't. But I use ClickHouse daily for columnar reporting, so the patterns are familiar.
```

### 6. Just to — clarification

Add 3–4 lines user can copy:

- `Just to confirm, you're asking about…, right?`
- `Just to clarify, do you mean… or…?`

### 7. Full scripts (rehearsal layer)

For each Word Plan question, add a **full paragraph** (60–120 sec spoken) in `*_interview_scripts.html`:

- Same facts as Word Plan — no new claims
- Natural B2 English, short sentences
- Mark section: `## Rehearsal script` under each question
- Derive wording from starters so the two layers stay aligned

**Practice ladder** (include in HTML callout):

1. Read full script aloud 2–3× (learn phrasing + facts)
2. Cover script; answer from Word Plan starters only 3–5×
3. On call: Word Plan or memory — not reading paragraphs

### 8. HTML deliverables

**Word Plan** — `applications/<slug>/<slug>_word_plan.html`:

1. JD pains table
2. Word Plans by question (starters only)
3. CAR skeletons
4. Yes/No table
5. Just to lines
6. Questions to ask recruiter (3–4)

**Scripts** — `applications/<slug>/<slug>_interview_scripts.html`:

1. Same question list as Word Plan
2. Full rehearsal paragraphs per question
3. Recruiter Q&A table (Yes/No + justification)
4. Link to Word Plan at top: *On the call, use Word Plan*

Print CSS: hide nav links — `@media print { .nav { display: none } }`

Templates: [reference.md](reference.md#html-template)

### 9. Practice instruction (always include)

```
Phase 1 (days before): rehearse with full scripts — aloud, 2–3 passes.
Phase 2 (day before / day of): Word Plan starters only — 3–5 passes.
On call: starters + your words. Scripts are backup notes, not a teleprompter.
```

## Chain with other skills

| Step | Skill |
|------|-------|
| Rate / tailor | `job-search-role-fit-rater`, `job-search-tailored-resume` |
| Facts | `PROFILE.md`, `storytellings.md` |
| **This skill** | Word Plan + optional full scripts (dual default) |
| Scripts (legacy) | `interview-prep-generator` — merge into dual output, don't duplicate conflicting facts |

## Prompt template

```text
Interview prep (dual) for <Company> <Role>.
Use job-search-interview-word-plan.

JD: <text or URL>
PROFILE: projects/job-search/career/PROFILE.md
Stories: projects/job-search/career/source-of-truth/storytellings.md
CV: projects/job-search/applications/<slug>/CV_*.md

Save both:
- applications/<slug>/<slug>_word_plan.html
- applications/<slug>/<slug>_interview_scripts.html
Link both from application hub.
```

`word plan only` — skip full script paragraphs, deliver Word Plan file only.
