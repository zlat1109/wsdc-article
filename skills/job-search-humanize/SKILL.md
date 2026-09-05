---
name: job-search-humanize
description: Strip AI-tells from cover letters, recruiter messages, and resume voice/format. Use after tailored resume or cover letter drafts, or when the user says humanize, less AI, sound like me. Paths under projects/job-search/career/.
metadata:
  origin: OriginalDopey/job-search-agent-skills (adapted)
---

# Job Search Humanize Pass

Post-process voice-critical drafts. **Not a generator** — rewrites existing text without changing claims or metrics.

## Project paths

- Profile (read-only): `projects/job-search/career/PROFILE.md`
- Format rules: `projects/job-search/career/RESUME-FORMAT-RULES.md`
- Cover letter archive: `projects/job-search/career/cover-letters/`
- Master resumes: `projects/job-search/resumes/`

## When to use

- After `job-search-tailored-resume` or `resume-tailor` / `cover-letter-generator`
- User pastes a draft and says "humanize" / "less AI"
- LinkedIn DM or recruiter reply drafts

## Do not run on

- `tracker/*.md`, `PROFILE.md`, skills sections (keyword density intentional)

## Full procedure

Read [reference/humanize-pass.md](reference/humanize-pass.md) and apply the content-type routing (cover letter vs resume summary vs bullets).

Always chain after tailored resume + cover letter generation in this workspace.
