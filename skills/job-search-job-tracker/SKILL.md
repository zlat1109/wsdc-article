---
name: job-search-job-tracker
description: Update job application pipeline and follow-ups in projects/job-search/career/tracker/. Use when user applied, got recruiter reply, wants pipeline status, or after role rating / resume tailoring.
metadata:
  origin: OriginalDopey/job-search-agent-skills (adapted)
---

# Job Tracker

Maintain source of truth:

- `projects/job-search/career/tracker/Applications.md`
- `projects/job-search/career/tracker/Pipeline.md`

Tailored artifacts live in `projects/job-search/applications/<company-slug>/`.

## Status vocabulary

Use exactly: `Backlog`, `Drafting`, `Ready`, `Applied`, `ATS-Screen`, `Recruiter-Screen`, `Hiring-Mgr-Screen`, `Phone`, `Technical`, `Onsite`, `Offer`, `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`

## Full procedure

Read [reference/job-tracker.md](reference/job-tracker.md).

Surface follow-ups (14+ days no response → consider `Ghosted`).
