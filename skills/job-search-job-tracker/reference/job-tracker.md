# Skill: Job Tracker

## Recommended model

`composer-2-fast` or `claude-haiku-4.x` — pure structured data entry. Cheapest tier is fine. Reasoning load is low; speed and cost matter.

## Purpose

Maintain `../tracker/Applications.md` and `../tracker/Pipeline.md` as your source of truth for every role you're evaluating, drafting, applying to, or interviewing for. Surface what needs follow-up. Drive the weekly review.

## When to Use This Skill

User says any of:
- "I just submitted to X"
- "I got a recruiter call back from Y"
- "Update my pipeline"
- "What should I follow up on?"
- "What's my status?"
- "Add this role to the tracker"
- After `role-fit-rater` or `tailored-resume-builder` — auto-update the tracker

## Status Vocabulary (Use Exactly These)

| Status | Meaning |
|--------|------|
| `Backlog` | Rated but not yet started — Apply or Stretch verdict in waiting |
| `Drafting` | Resume + cover letter being built |
| `Ready` | Resume + cover letter built, not yet submitted |
| `Applied` | Submitted via portal / email / referral |
| `ATS-Screen` | Auto-rejected or moved through ATS |
| `Recruiter-Screen` | Talked to recruiter |
| `Hiring-Mgr-Screen` | Talked to hiring manager |
| `Phone` | Phone interview scheduled or done |
| `Technical` | Technical / take-home / panel done |
| `Onsite` | Final-round / onsite done |
| `Offer` | Offer in hand |
| `Accepted` | Offer accepted |
| `Rejected` | Rejected at any stage |
| `Withdrawn` | Candidate pulled out |
| `Ghosted` | No response 14+ days after last contact |
| `Skip` | Rated Skip — don't apply |

## Applications.md Schema

The table has these columns. Maintain exactly. Use ISO `YYYY-MM-DD` for dates.

```
| ID | Date Added | Date Last Update | Company | Role | Req# | Comp Band | Verdict | Status | Resume # | Cover Letter | Recruiter | Next Action | Notes |
```

- **ID** = sequential `A001`, `A002`, etc.
- **Verdict** = `Apply` / `Stretch` / `Skip` (from role-fit-rater)
- **Resume #** = the file number from `NN-...md` (e.g., `05` for Director EA). `—` if Skip.
- **Cover Letter** = the section heading in `../resumes/09-Cover-Letter-Templates.md`. `—` if Skip.

After the table, maintain a **Status Timeline** section at the bottom of the file:

```
## Status Timeline

- 2026-05-15 · A001 Company X Senior Engineer · Backlog → Ready (resume #05 built)
- 2026-05-16 · A002 Company Y Staff Architect · Backlog → Drafting
```

This is the audit trail. Append-only. Never edit historical entries.

## Pipeline.md Schema

Status-grouped *view* of Applications.md. Regenerate from Applications.md whenever it's out of date. Group by Status; within each group, sort by `Date Last Update` descending.

Sections to maintain:
- `## Active` — anything in `Drafting`, `Ready`, `Applied`, `Recruiter-Screen`, `Hiring-Mgr-Screen`, `Phone`, `Technical`, `Onsite`, `Offer`
- `## Backlog` — `Backlog` only
- `## Closed` — `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`, `ATS-Screen`
- `## Skipped` — `Skip` only

Each row keeps the same columns as Applications.md.

## Operations

### Add a new role
1. Append a row to `Applications.md` with the next ID and `Date Added = today`.
2. Set `Verdict` from the role-fit-rater output.
3. Set `Status = Backlog` if Apply/Stretch but not yet started; `Status = Skip` if Skip.
4. Update Pipeline.md.
5. Append to Status Timeline: `YYYY-MM-DD · <ID> <short name> · — → Backlog`.

### Status change
1. Update the row's `Status` and `Date Last Update = today`.
2. Update `Next Action` and `Notes` as appropriate.
3. Update Pipeline.md (move the row to the new section).
4. Append a Status Timeline line.

### Recruiter contact
1. Update `Recruiter` column with name + email/phone.
2. Update `Notes` with the conversation summary.
3. Set `Next Action` and a date in `Date Last Update`.

### Pipeline check ("what should I follow up on?")
1. From Pipeline.md → Active section: surface anything where `Date Last Update` is more than the threshold below.
2. Threshold by status:
   - `Applied`: 7 days → "follow up with recruiter"
   - `Recruiter-Screen`: 5 days → "follow up on next steps"
   - `Phone`: 5 days → "thank-you note + ask for status"
   - `Technical` / `Onsite`: 5 days → "thank-you + ask for decision date"
   - `Offer`: 3 days → "respond / negotiate"
3. Surface as a checklist with the action and the contact.

## Weekly Review

Every Friday (see `../tracker/Weekly-Review.md`):
1. Run pipeline check (above).
2. Count: `Applied this week`, `Interviews this week`, `Roles in Backlog`, `New roles added this week`.
3. Suggest: which Backlog role to promote next based on best Apply verdict + comp band + freshness.
4. Reference `../tracker/Career-Motivators.md` if filled — does the current pipeline align with your top-3 motivators? If not, surface that.

## Anti-Patterns

- Do **not** edit historical Status Timeline entries — it's an audit trail
- Do **not** delete rows from Applications.md — change Status to `Withdrawn` or `Skip` instead
- Do **not** track confidential salary expectations in this file (recruiter conversation only)
- Do **not** include recruiter personal details that would create a privacy concern if the file is shared

## See Also

- `role-fit-rater.md` — produces the Verdict that lands in the tracker
- `tailored-resume-builder.md` — creates resume + cover letter, tracker updates after
- `network-mapper.md` — for outreach planning
- `../tracker/Weekly-Review.md` — weekly check-in template
