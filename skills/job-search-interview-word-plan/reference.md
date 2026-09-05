# Word Plan — reference

## Universal starter phrases (BI / Data / Analytics)

### About you / current role
- In my current role, I was responsible for…
- I own the BI layer of…
- Day to day, I work with…
- One thing I'm proud of in this role is…

### Projects / cases
- One project I'm proud of is…
- The challenge was that…
- What I did first was…
- As a result, we managed to…
- The main outcome was…

### Fit / motivation
- What caught my attention in this role is…
- That connects to what I do today around…
- From the job description, it sounds like you need…

### Gaps (honest)
- I want to be transparent: …
- I haven't used X in production, but I use Y, which is similar because…
- I'm confident I can ramp up because…

### Clarification (Just to)
- Just to confirm, you're asking about…, right?
- Just to clarify, do you mean… or…?
- Just to make sure we're aligned, …

### Closing interest
- Thank you — I'm interested in moving forward.
- This role matches my background in…

---

## CAR skeleton template

```markdown
### [Story name]

**Challenge:** [One sentence — situation]

**Action:**
- [Step 1 — what YOU did]
- [Step 2]
- [Step 3]

**Result:** [Metric from PROFILE only — who benefited, what improved]
```

---

## Yes / No formula

`Yes/No` + **one sentence** (justification or clarification).

| Question type | Pattern |
|---------------|---------|
| Tool experience | Yes, I have. At [company], I [scope]. |
| No experience | No, I haven't. But I've [adjacent]. So I could learn quickly. |
| Applying elsewhere | Yes, I'm in a few processes. [Company] is a priority because [JD fit]. |
| Salary | I'm looking at around [X]. May I ask what range is budgeted? |

---

## JD pain mining template

```markdown
| JD phrase | Likely pain | Your evidence (PROFILE) | Intro / answer hook |
|-----------|-------------|-------------------------|---------------------|
| … | … | … | Starter phrase to use |
```

---

## HTML template

Minimal structure for `*_word_plan.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Company] — Word Plan</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 0 auto; padding: 1.5rem; line-height: 1.5; }
    h2 { font-size: 1rem; text-transform: uppercase; color: #555; border-bottom: 1px solid #ddd; }
    .starters { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 0.75rem 1rem; margin: 0.5rem 0; }
    .starters li { margin: 0.35rem 0; font-style: italic; }
    .warn { background: #fff7ed; padding: 0.75rem; font-size: 0.9rem; }
    table { width: 100%; font-size: 0.9rem; border-collapse: collapse; }
    th, td { border-bottom: 1px solid #eee; padding: 0.4rem; text-align: left; vertical-align: top; }
    @media print { .nav { display: none !important; } }
  </style>
</head>
<body>
  <p class="nav"><a href="[hub].html">← Pack hub</a></p>
  <h1>[Company] — Word Plan</h1>
  <p class="warn"><strong>On the call:</strong> use starters only. Speak aloud — do not read paragraphs.</p>

  <h2>JD pains</h2>
  <!-- table -->

  <h2>Q1: Tell me about yourself</h2>
  <ul class="starters">
    <li>In my current role, I…</li>
  </ul>

  <h2>CAR — [story name]</h2>
  <!-- Challenge / Action bullets / Result -->

  <h2>Yes / No</h2>
  <!-- table -->

  <h2>Just to</h2>
  <ul><!-- clarification lines --></ul>
</body>
</html>
```

---

## Impact — "So what?" (no lying)

Before adding a metric to spoken prep, ask:

1. I did X — **so what?**
2. Who benefited?
3. What improved (time, trust, speed, fewer requests)?

Use only numbers confirmed in PROFILE. Non-business impact is valid (e.g. "teams trusted the metrics more", "self-service reduced ad-hoc load").

---

## Dual-mode practice ladder

| Phase | Material | Goal |
|-------|----------|------|
| 1 — Learn | Full script | Fix wording, facts, timing (60–120 sec) |
| 2 — Internalize | Word Plan starters | Speak without reading paragraphs |
| 3 — Call | Word Plan (or memory) | Natural delivery under stress |

If full scripts help you: use Phase 1 longer. Still run Phase 2 before the call — scripts become a crutch if you skip it.

---

## Solo practice (5–10 min)

1. **With script:** read one answer aloud; note phrases you like → copy best opener into Word Plan if missing.
2. **Without script:** say only the first starter; continue 60–90 sec in your own words.
3. Repeat with a different starter for the same question.

Do **not** read the full paragraph on screen during the actual call unless you consciously choose that fallback.

---

## Combined hub snippet

Link both files from `*_career_os_result.html`:

```html
<li><a href="<slug>_word_plan.html">Word Plan (on call)</a></li>
<li><a href="<slug>_interview_scripts.html">Full scripts (rehearsal)</a></li>
```
