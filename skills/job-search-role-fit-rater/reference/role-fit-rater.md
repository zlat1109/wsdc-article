# Skill: Role Fit Rater

## Recommended model

`claude-sonnet-4.x` or `gpt-5-mini` — structured rubric scoring, no voice-critical generation. Mid-tier is the sweet spot for cost vs reasoning quality on the Apply/Stretch/Skip judgment calls.

## Purpose

When the user shares a JD, URL, or list of roles, produce a clean **Apply / Stretch / Skip** verdict for each, anchored to the candidate's profile in `../PROFILE.md` and (if filled) their Career Motivators.

## When to Use This Skill

User says any of:
- "Is this a fit?"
- "Rate these roles"
- "Should I apply to this?"
- Pastes a JD or URL list and asks anything
- Asks "what should I focus on?"

## Output Format

Always produce a Markdown table with the columns:

| # | Role / Req# | Comp | Verdict | Resume Variant | Reason |

Use these verdict labels exactly:
- `✅ Apply` — strong fit, build a tailored resume + cover letter
- `🟡 Stretch` — real fit but with disclosed gaps; only apply if user wants the comp/brand/strategic fit
- `❌ Skip` — domain mismatch, hard blocker (cert / clearance / location), or significantly underleveled

After the table, list the **top 1–3 to apply to first** and one-line each.

## Rating Rubric — Apply (✅)

The role is an Apply if **at least 4** of these are true:

1. **Title altitude is right** — within one level of your current title (up or lateral). Check `PROFILE.md` target titles.
2. **Domain matches** — the role's domain is in your `PROFILE.md` target domains list OR is closely adjacent.
3. **No hard blocker:** required cert/degree/clearance you don't have and can't work around, or location-locked hybrid that conflicts with your location.
4. **Comp band reaches your floor** (from `PROFILE.md`) OR the role offers strategic brand value that justifies a stretch comp.
5. **JD evidence maps to ≥3 of your key accomplishments** from `PROFILE.md` (i.e., you have proof, not just proximity).
6. **Industry is fluent for you** — you've worked in or sold into this industry before.

## Rating Rubric — Stretch (🟡)

The role is a Stretch if it would be Apply **except**:
- Comp band is below your target (note in cover letter — request flex)
- A specific cert/skill is missing but adjacent foundation is strong (note in cover letter — commit to ramp)
- Domain is adjacent but not core (note in cover letter — disclose honestly)
- Pre-identified-candidate signal in the JD (treat as Skip *unless* unusually well-aligned)

## Rating Rubric — Skip (❌)

Skip if any:
- Hard cert blocker (required degree/cert you don't have and can't flex)
- Pure-domain-specialist role outside your career history
- Significantly underleveled (2+ levels below current)
- Location-locked onsite that conflicts with your location and you can't relocate
- Pre-identified candidate disclosed in JD

## Workflow

1. Read the JD content (fetch URL if not already provided).
2. Read `../PROFILE.md` — the candidate's profile, accomplishments, target criteria.
3. For each role, score against the rubric above.
4. Produce the verdict table.
5. List the top 1–3 to apply to first.
6. **For each Apply:** name the closest existing resume variant from `../resumes/`. If no existing variant fits, note "needs new variant via tailored-resume-builder skill".
7. Update `../tracker/Applications.md` with one row per role (status = `Backlog` for not-yet-applied, plus the verdict).
8. Ask: "Want me to build the tailored resume(s) for the Apply roles?"

## Honest-Caveat Surfacing

When you spot a stretch, surface the gap up front, do not paper over it. Examples:
- "Pre-identified candidate disclosed — strong signal the posting is a formality. Skip."
- "Comp band $92K–$148K is below your target. Apply only if the brand / context is strategic."
- "PROSCI required without flex. Contact recruiter to confirm equivalency before burning the application."

## Anti-Patterns (Things This Skill Should NOT Do)

- Do **not** invent JD content. If JD fetch fails, say so and offer to retry or work from title alone with caveat.
- Do **not** use generic praise ("strong fit"). Always cite the specific JD bullet that maps to a specific accomplishment from `PROFILE.md`.
- Do **not** rate a role Apply if there's a hard blocker just because the rest is good.
- Do **not** skip the comp-gap conversation when the band is below target.

## Example Output

```
| # | Role | Comp | Verdict | Resume | Reason |
|---|------|------|---------|--------|--------|
| 1 | Acme Corp — Senior Platform Engineer (R-12345) | $160K–$200K | ✅ Apply | 05 | Platform infra + team leadership + your Kubernetes migration maps directly. |
| 2 | BigCo — Junior DevOps Analyst (R-67890) | $75K–$95K | ❌ Skip | — | Underleveled (2+ levels below). Comp below floor. |
| 3 | StartupX — Staff Engineer (no req#) | $180K–$220K | 🟡 Stretch | 03 | Strong tech fit but domain is adtech (adjacent, not core). Disclose in cover letter. |

Top 3 to apply first:
1. Acme Corp (#1) — strongest platform-engineering match
2. StartupX (#3) — stretch but comp is excellent and role is high-autonomy

Want me to build the tailored resumes for the Apply roles?
```

## See Also

- `tailored-resume-builder.md` — invoked next for each Apply
- `job-tracker.md` — invoked to record verdicts
- `../PROFILE.md` — candidate's source of truth
