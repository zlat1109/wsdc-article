---
name: job-search-role-fit-rater
description: Rate a job description Apply / Stretch / Skip against the candidate profile. Use when user pastes a JD, asks if they should apply, or wants role prioritization. Reads projects/job-search/career/PROFILE.md.
metadata:
  origin: OriginalDopey/job-search-agent-skills (adapted)
---

# Role Fit Rater

Produce **Apply / Stretch / Skip** verdicts anchored to `projects/job-search/career/PROFILE.md` and optional `projects/job-search/career/tracker/Career-Motivators.md`.

## Output table

| # | Role / Req# | Comp | Verdict | Resume Variant | Reason |

Verdicts: `✅ Apply` | `🟡 Stretch` | `❌ Skip`

After the table: top 1–3 to apply first.

## Full rubric

Read [reference/role-fit-rater.md](reference/role-fit-rater.md).

## After rating

- **Apply / Stretch** → suggest `job-search-tailored-resume` or `resume-tailor`
- Update `projects/job-search/career/tracker/Applications.md` via `job-search-job-tracker`
