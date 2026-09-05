# Skill: Tailored Resume Builder

## Recommended model

`claude-opus-4.x` or `gpt-5` for the initial draft. Voice quality and evidence accuracy are both critical here; this is not the place to save cost.

**Always followed by `humanize-pass.md` on a mid-tier model** before the artifact is considered done.

## Purpose

Build a resume + matching cover letter for a specific target role. Reuse the closest existing variant as the base, reorder bullets and Skills for the JD's keywords, and disclose any honest gaps openly.

## When to Use This Skill

User says any of:
- "Build me a resume for this role"
- "Tailor for X"
- "I want to apply to Y"
- After `role-fit-rater` produced an Apply or Stretch verdict

## Inputs Needed

1. **Target role** — title, company, requisition number, comp band, location.
2. **JD content** — fetch the URL if not pasted. If fetch fails, work from title + adjacent JDs and add a `note:` in YAML disclosing this.
3. **Honest gaps** — what's missing? Cert? Domain? Comp band below trajectory?

## Output Files

For each tailored resume, produce **two files**:

1. **`NN-<Category>-<Role>.md`** — resume Markdown (next available `NN`, see existing files for the convention).
2. **A new section appended to `../resumes/09-Cover-Letter-Templates.md`** with the matching cover letter.

Then update `../tracker/Applications.md`.

## Resume Structure (Standardized Convention)

```yaml
---
title: "[Your Name] — <Role Title>"
target_role: "<Company> / Req <ID> — <Role Title> (<comp band>, <location>)"
target_jd_url: "<URL>"
target_jd_source: "<recruiter email / job board / referral>"
note: "<optional caveats e.g. JD fetch timed out>"
geometry: "margin=0.6in"
fontsize: 10pt
mainfont: "Calibri"
---
```

```markdown
**[YOUR FULL NAME]**

[Address] · [City, State ZIP] · [Phone] · [Email] · [LinkedIn URL]

**[Top 3 most-relevant credentials, dot-separated]**

**PROFESSIONAL SUMMARY**

[ONE paragraph, ~120 words. Third-person / no-person voice. NO "I", NO contractions. Lead with role-class noun phrase. End with 1-2 short factual sentences like "Computer Science degree (MIT). Strong communicator and technical leader."]

**EXPERIENCE**

**[Start Date] -- [End Date or Present]** [Company] \| [Location]

**[Title]**

- [5-7 bullets max for current role. Outcomes, not technical-stack detail. Mix of lead verbs.]

**[Start Date] -- [End Date]** [Previous Company] \| [Location]

**[Title]**

- [Lead bullet: key accomplishments + metrics]
- [4 bullets max for older roles]

**SKILLS**

- **[Most-relevant category]:** [keyword-loaded for the target ATS]
- **Programming Languages:** ...
- **Cloud & Infrastructure:** ...
- **[Other relevant categories]:** ...

**PROFESSIONAL DEVELOPMENT**

- [List certifications, lead with most-relevant for this role]

**PROFESSIONAL AWARDS**

- [Your awards — include all that are relevant]

**EDUCATION**

[School] \| [City, State]

**[Degree]**

**EXTRA-CURRICULAR**

- [Memberships, volunteer work, etc.]
```

### Critical format rules (do not deviate)

1. **Section headers** are `**ALL CAPS BOLD**` lines, NOT `##` markdown headings. Pandoc renders `##` as H2 styling that looks wrong in a Word resume.
2. **Header layout:** Bold name on its own line. Single dot-separated contact line. Single bold credentials line (top 3 only). NO H1 (`# Name`).
3. **Experience entries:** Date FIRST in bold, then company, then location. Title on next bold line.
4. **Education entries:** School name + location on one line (plain text), bold degree on next line.
5. **No "References available upon request" footer.** Drop it.
6. **No "Affiliations" header.** Use **EXTRA-CURRICULAR**.
7. **Section order:** Professional Summary → Experience → Skills → Professional Development → Professional Awards → Education → Extra-Curricular.

### Voice rules — Resume Professional Summary

- **NO first-person.** No "I", "I've", "I'd", "I'm", "I will", etc.
- **NO contractions.** "I've" / "I'd" / "won't" do not belong here.
- **ONE paragraph, ~120 words max.** No paragraph break.
- **NO "Combines X with Y" pattern.** NO "Brings the rare combination."
- **End with 1-2 short factual sentences** (degree, communication strength, etc.)

### Voice rules — Resume Bullets

- **Cap current-role bullets at 5-7.** Past-role bullets at 4 max.
- **Outcomes, not stacks.** What does it do for the business? Not what it's built from.
- **Vary lead verbs.** No three in a row starting the same.
- **No em dashes.** Use commas, hyphens, or spaced single dashes (" - ") instead.
- **Drop excessive bolding.** Bold the artifact name and the metric. Not every other phrase.

## Build Workflow

1. **Pick the closest existing variant** from `../resumes/`. If this is your first resume, use `00-Resume-Template.md` as the scaffold.
2. **Copy** that variant's content as the starting point.
3. **Update YAML front-matter** (`title`, `target_role`, `target_jd_url`, `target_jd_source` if from a recruiter email, `note` if needed).
4. **Apply the format template above:** ALL CAPS BOLD section headers, bold-name header, date-first experience entries, bold-degree education, no References footer.
5. **Rewrite Professional Summary** in third-person/no-person voice (~120 words, one paragraph). Do NOT add "I" or contractions to the resume PS. Lead with role-class noun phrase. Match the target's "shape":
   - Executive vs IC level
   - Vendor-side vs customer-side framing
   - Technical-depth vs strategic framing
6. **Reorder bullets under current experience.** Put the bullets that map to JD requirements first. Cap at 5-7 bullets. Each bullet leads with an outcome, not a tech-stack inventory.
7. **Pull JD keywords into Skills** in order of importance.
8. **Sanity check page count.** ~2 pages in 10pt Calibri / 0.6" margins. If long: drop the lowest-relevance older-role bullets.
9. **Append matching cover letter** to `../resumes/09-Cover-Letter-Templates.md`. ~350–400 words. Cover letter VOICE is different from resume voice — keep first-person, contractions, and personal asides. Structure:
    - Opening: which role + 1-line "why I want this" (vary opener)
    - 4–6 bulleted direct mappings ("JD says X, I shipped Y")
    - Honest-disclosure section if there are gaps — call them out in plain language
    - Optional: "Happy to share <work sample> as evidence" (vary closer)
    - Sign off (vary; never default to "Best regards")
10. **Update `../tracker/Applications.md`** — set status to `Drafting` once the resume is built; status to `Ready` once humanized; status to `Applied` once the user actually submits.
11. **Run `humanize-pass.md`** on the new cover letter section (and on the resume's Professional Summary if you accidentally introduced first-person/contractions while drafting).

## Auditability Rule (Critical)

**Every metric in every bullet must trace to `../PROFILE.md`** (your source of truth with key accomplishments and employment history).

If you want to add a number that isn't sourced, **stop and ask the user** to confirm and then update `PROFILE.md` first so it's traceable.

## Honest-Gap Disclosure

For every Stretch role, the cover letter must include a "**Honest disclosures**" or "**Honest note**" subsection that:
- Names the gap (e.g., "Kubernetes certification not yet held")
- Says what you have instead (e.g., "3 years of production Kubernetes operation, deep EKS familiarity, just haven't sat the exam")
- Commits to a path forward (e.g., "Willing to pursue CKA certification immediately upon hire")

Recruiters trust honesty. Don't paper over.

## Anti-Patterns

- Do **not** start from scratch when a close variant exists — start from the closest tailored variant
- Do **not** produce a 3-page resume — drop bullets if needed
- Do **not** invent metrics
- Do **not** forget to update `../tracker/Applications.md`

## See Also

- `role-fit-rater.md` — produces the Apply verdict that triggers this skill
- `job-tracker.md` — invoked to update Applications.md after build
- `humanize-pass.md` — post-processing step to strip AI-tells
- `../PROFILE.md` — source of truth for all claims
