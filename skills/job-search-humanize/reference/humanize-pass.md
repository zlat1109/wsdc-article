# Skill: Humanize Pass

## Recommended model

`claude-sonnet-4.x` or `gpt-5-mini` — pattern removal and rewriting against a checklist. No need for premium-tier reasoning here. This skill is the *cost saver* for the dossier: do voice-critical generation on premium, then humanize on mid-tier.

## Purpose

Take any voice-critical draft (cover letter, LinkedIn DM, recruiter reply, **OR** a resume that needs format/voice cleanup) and strip the AI-tells. **The rules differ by content type** — applying cover-letter voice to a resume produces something unusable. Route correctly.

This is a **post-processing step**, not a generator. The draft already exists; this skill rewrites it for voice/format without touching the underlying claims, metrics, or structure.

## Content-type routing (read this first)

| Content type | What humanize-pass does | What it does NOT do |
|---|---|---|
| **Cover letter** | Adds first-person + contractions, varies opener/closer/sign-off, strips all em dashes (replace with commas/hyphens/spaced dashes), removes AI-tell phrases | Doesn't touch metrics, doesn't soften gap disclosures, doesn't change structure |
| **LinkedIn DM / outreach** | Same as cover letter, plus enforces personalization line and zero-em-dash rule | Doesn't generate new content from scratch |
| **Resume Professional Summary** | **STRIPS first-person and contractions**, enforces ALL CAPS section header, single-paragraph rule, length cap (~120 words), removes "Combines X with Y" / "Brings the rare combination" patterns | Doesn't touch bullets unless format is wrong |
| **Resume Experience entry** | Format-only: ensures date-first format, ensures no `##` markdown heading | Doesn't rewrite bullet content unless lead-verb-repeats are obvious |
| **Resume bullets** | Lead-verb variation only; trim to ≤7 if over | Doesn't change metrics or claims |
| **Recruiter reply email** | Same as cover letter | Doesn't change attached files, dates, or questions |

## When to Use This Skill

Run it automatically after:
- `tailored-resume-builder.md` produces a new resume or cover letter
- A new LinkedIn DM is drafted
- A recruiter reply is composed
- The user pastes a draft and says "make this sound less AI"
- Any voice-critical artifact has been edited substantively

Do **not** run it on:
- `Applications.md`, `Pipeline.md`, `Network.md` — these are structured trackers
- `PROFILE.md` — source of truth
- The Skills section of resumes (keyword density is intentional)
- Bullets in the Experience section (action-verb density is expected; only fix lead-verb repeats)

## Workflow

1. **Read the draft.** Identify the content type (cover letter / DM / resume PS / resume Experience entry / etc.) and route to the matching rule set.

2. **For cover letters and DMs — audit against COVER LETTER rules:**
   - Em dashes (0 everywhere - replace with commas, hyphens, or spaced single dashes)
   - `**Bold noun**, **Bold noun**, **Bold noun**` chains in body prose
   - `not X, but Y` constructions
   - Triadic constructions (X, Y, and Z)
   - Banned phrases ("leveraging," "delve into," "robust," "comprehensive," "seamless," "cutting-edge," "landscape," "Combines X with Y," "Brings the rare combination")
   - First-word verb repeats in consecutive bullets
   - Contractions per paragraph (must be ≥1)
   - First-person aside per cover letter (must be ≥1)
   - Opener variety vs other letters in the same dossier
   - Closer variety vs other letters in the same dossier
   - Sign-off variety vs previous letter

3. **For resumes — audit against RESUME rules:**
   - Section headers are `**ALL CAPS BOLD**`, not `## Markdown`
   - Header layout is bold-name + single-line contact + bold credentials line (no `# H1`)
   - Experience entries are date-first format
   - Education is school+location plain text + bold degree
   - No "References available upon request" footer
   - Affiliations section is renamed `**EXTRA-CURRICULAR**`
   - Professional Summary is ONE paragraph, ≤~120 words
   - Professional Summary has ZERO first-person pronouns and ZERO contractions
   - Professional Summary doesn't use "Combines X with Y" or "Brings the rare combination"
   - Bullet count for current role is ≤7
   - No three consecutive bullets starting with the same verb

4. **Rewrite to fit the relevant rule set.** Specific moves:

   **Em dash → period, comma, or spaced hyphen.** Break long em-dash chains into shorter sentences. No em dashes in any output.

   **Bold-noun chains → mixed prose.** Drop excessive bolds in body prose; keep them in bullets where they cue the eye.

   **`not X, but Y` → flatter statement.** "ships production automation, not slideware" → "ships production automation. Slideware doesn't survive code review."

   **Triadic packing → list or two pairs.** "Combines deep technical execution, executive-grade governance, and 8+ years of presales depth" → "Combines deep technical execution with executive governance design. Eight years of presales depth on top."

   **Lead-verb repeats → variety pull.** Three consecutive bullets starting with "Owned" → vary to "Owned... / Built... / Shipped..."

   **AI-shape opener → natural opener.** Vary the opening line style. Match the opener to the role's tone (sales role gets a punchier opener; compliance role gets a steadier one).

5. **Insert at least one personal aside in cover letters.** Find a natural place to drop one of:
   - The "as my actual title" turn (works for any role you've been doing de facto)
   - The "I've been the customer" turn (works for any vendor / SE / CSM role)
   - A candid line about the gap ("comp-band conversation aside, the work fits")
   - A dry one-liner that sounds like a human wrote it, not a model

6. **Cycle the closer and sign-off.** Reference other letters in the dossier; pick a closer + sign-off pair you haven't used recently.

7. **Re-read aloud (mentally).** Does it sound like a person? If two consecutive sentences feel the same length, vary one.

8. **Save.**

## Output Format

Return either:
- The rewritten artifact in full, OR
- A diff-style before/after for spot-checks

For batch jobs (e.g., "humanize all my cover letters"), produce:

```
## Letter 1: [name]
- Em-dash count: [before] → [after]
- Opener change: "[old]" → "[new]"
- Sign-off change: [old] → [new]
- Asides added: [count]
- Other notes: [any judgment calls]
```

Then save the rewrites.

## Critical: Do NOT Touch

- Any number, metric, or proper noun (verify against `../PROFILE.md`)
- The structure (sections, bullets, headers) — only the prose
- Honest-disclosure content (the gap acknowledgment is the most important paragraph in the letter; rewrite the *form* but never soften the *substance*)
- The `[Hiring Manager / Recruiter Name]` and `[Company]` placeholders

## Anti-Patterns

- Do **not** introduce filler ("I'm thrilled," "passionate") in the name of "humanizing"
- Do **not** make the writing breezy or folksy — aim for dry, candid, low-key confident
- Do **not** remove technical specificity to "smooth" the prose
- Do **not** generate fresh claims — only rewrite existing ones

## Examples

### Cover letter — Before / After

**Before (typical AI-shape opener):**

> Dear [Hiring Manager],
> 
> I'm applying for the Director of Engineering role at [Company]. I bring a comprehensive background in platform infrastructure — and the proof is in production today.
> 
> Highlights:
> - **Kubernetes migration.** Led migration of 200+ microservices from on-prem to EKS across a 40-person engineering org...

**After (humanized):**

> Dear [Hiring Manager],
> 
> Quick context before the resume: I've been running platform migrations for 200+ service orgs for three years, and the role you've posted is what I've been doing without the title.
> 
> Three things to call out:
> 
> - **Kubernetes migration.** Led the move of 200+ microservices from on-prem to EKS across a 40-person engineering org...

Em dash count: 0 (as required). Opener varied. "Three things to call out" replaces "Highlights:" pattern. Personal aside added ("without the title"). Same content, same metrics, same honest disclosures.

### Resume Professional Summary — Before / After

**Before (cover-letter voice incorrectly applied to a resume PS):**

> ## Professional Summary
> 
> I'm a platform engineer with **deep Kubernetes expertise** and **5 years leading infrastructure teams**. I've migrated 200+ services to the cloud and I'm passionate about developer experience...

**After (correct resume voice):**

> **PROFESSIONAL SUMMARY**
> 
> Platform engineer and infrastructure leader with 5 years of team leadership and deep Kubernetes expertise. Production record includes 200+ service migrations to EKS, developer platform design for 40-person engineering orgs, and CI/CD pipeline standardization across three business units. Computer Science degree (Stanford). Strong technical communicator.

Changes:
- Section header: `## Professional Summary` → `**PROFESSIONAL SUMMARY**`
- Removed "I'm" / "I've" / first-person entirely
- Removed "passionate" (banned filler)
- Collapsed to one paragraph, depersonalized voice
- Added factual closer

## See Also

- `../RESUME-FORMAT-RULES.md` — the full format reference
- `tailored-resume-builder.md` — the upstream skill that produces drafts to humanize
- `../PROFILE.md` — source of truth for verifying claims
