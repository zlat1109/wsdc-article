---
name: job-search-tailored-resume
description: Build tailored resume and cover letter for a specific role from PROFILE.md and master resume. Saves to projects/job-search/applications/. Always chain job-search-humanize after. Use after Apply/Stretch verdict.
metadata:
  origin: OriginalDopey/job-search-agent-skills (adapted)
---

# Tailored Resume Builder (job-search)

## Inputs

1. Target role (title, company, comp, location, JD URL or text)
2. `projects/job-search/career/PROFILE.md`
3. Closest master: `projects/job-search/resumes/Resume_Balakin_Denis_EU_EN.md` (or RU variant if requested)
4. Format: `projects/job-search/career/RESUME-FORMAT-RULES.md`

## Outputs

1. `projects/job-search/applications/<company-slug>/CV_<Company>_EN.md` (or agreed name)
2. Append cover letter to `projects/job-search/career/cover-letters/00-Cover-Letter-Templates.md` **or** `applications/<slug>/Cover_Letter.md`
3. Update `projects/job-search/career/tracker/Applications.md`

## Rules

- **No invented bullets, metrics, or employers** — only PROFILE + master resume facts
- Reorder bullets and skills for JD keywords (ATS)
- EU/UK format: 2 pages OK; city only; no photo; visa note if relevant (Spain EU permit)

## Full structure

Read [reference/tailored-resume-builder.md](reference/tailored-resume-builder.md).

## Mandatory next step

Run **`job-search-humanize`** on cover letter and resume Professional Summary before marking `Ready`.
