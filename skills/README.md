# Cursor Skills Guide

This directory contains Agent Skills - reusable instructions that teach the AI how to perform specific tasks.

## Structure

```
~/.cursor/skills/
├── code-review/
│   └── SKILL.md
├── database-analysis/
│   └── SKILL.md
├── tableau-workflows/
│   └── SKILL.md
├── project-setup/
│   └── SKILL.md
├── web-development/
│   └── SKILL.md
├── taste-skill/                # Leonxlnx anti-slop UI
│   └── SKILL.md
├── redesign-skill/             # audit + improve existing UI
│   └── SKILL.md
├── emil-design-eng/            # Emil Kowalski motion
│   └── SKILL.md
├── testing/
│   └── SKILL.md
├── python-development/
│   └── SKILL.md
├── cursor-orchestration/
│   └── SKILL.md
├── agents-best-practices/
│   ├── SKILL.md
│   └── references/
├── thermo-nuclear-code-quality-review/
│   └── SKILL.md
├── article-writing/          # from ECC cherry-pick
│   └── SKILL.md
├── brand-voice/              # companion for article-writing
│   ├── SKILL.md
│   └── references/
├── search-first/
│   └── SKILL.md
├── documentation-lookup/
│   └── SKILL.md
├── verification-loop/
│   └── SKILL.md
└── eval-harness/
    └── SKILL.md
├── job-description-analyzer/     # ResumeSkills
├── resume-tailor/
├── cover-letter-generator/
├── resume-ats-optimizer/
├── resume-bullet-writer/
├── interview-prep-generator/
├── tech-resume-optimizer/
├── resume-cover-letter/          # jezweb EU/US/UK
├── job-search-humanize/
├── job-search-role-fit-rater/
├── job-search-tailored-resume/
└── job-search-job-tracker/
├── workspace-hygiene-audit/    # folder/log audit (custom)
├── workspace-surface-audit/    # ECC harness audit
├── skill-stocktake/            # ECC skills quality
└── refactor-clean/             # ECC dead code
├── grill-me/                   # RobMitt — stress-test plan before code
├── process-interviewer/        # Mafia-Claude-Skills — interview before build
├── prompt-master/              # smusman437 — chaotic input → prompt
├── humanizer/                  # blader — remove AI writing patterns
├── linkedin-hook-generator/    # aiskilloftheweek — LinkedIn opening lines
├── fact-checker/               # seaworld008 — verify claims before publish
└── gsd-orchestration/          # NatiLevyy — spec-driven plan A→Z
```

## What Are Skills?

Skills are markdown files that teach the agent specialized workflows:
- Code review using team standards
- Database analysis and optimization
- Tableau dashboard creation
- Project setup and scaffolding
- Web development (HTML, CSS, JavaScript)
- Testing (Python, web, SQL)
- Python development (web scraping, data processing, API integration)
- Cursor orchestration (which Skill/MCP/Rule to use per task)

Skills are automatically discovered and applied when relevant to the task.

## Skill Structure

Each skill is a directory containing `SKILL.md`:

```
skill-name/
├── SKILL.md              # Required - main instructions
├── reference.md          # Optional - detailed documentation
├── examples.md           # Optional - usage examples
└── scripts/              # Optional - utility scripts
    ├── validate.py
    └── helper.sh
```

## SKILL.md Format

Every skill requires a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it
---

# Skill Name

## Instructions
Clear, step-by-step guidance for the agent.

## Examples
Concrete examples of using this skill.
```

## Writing Effective Descriptions

The description is **critical** - the agent uses it to decide when to apply your skill.

### Best Practices

1. **Write in third person**:
   - ✅ Good: "Reviews code for quality and security"
   - ❌ Bad: "I can help you review code"

2. **Be specific and include trigger terms**:
   - ✅ Good: "Analyzes SQL queries and optimizes performance. Use when working with SQL, databases, or query optimization."
   - ❌ Bad: "Helps with databases"

3. **Include both WHAT and WHEN**:
   - WHAT: What the skill does (specific capabilities)
   - WHEN: When the agent should use it (trigger scenarios)

### Description Examples

```yaml
# Code Review
description: Reviews code for quality, security, and maintainability following team standards. Use when reviewing pull requests, examining code changes, or when the user asks for a code review.

# Database Analysis
description: Analyzes SQL queries, database schemas, and data structures. Optimizes queries, identifies performance issues, and provides data insights. Use when working with SQL, databases, data analysis, or query optimization.

# Tableau Workflows
description: Works with Tableau workbooks, dashboards, and data sources. Creates visualizations, optimizes performance, and manages Tableau projects. Use when working with Tableau, .twb/.twbx files, dashboards, or data visualization.
```

## Creating New Skills

### Step 1: Create Directory

```bash
mkdir -p ~/.cursor/skills/my-skill
```

### Step 2: Write SKILL.md

Create `SKILL.md` with:
- YAML frontmatter (`name`, `description`)
- Clear instructions
- Concrete examples
- Under 500 lines

### Step 3: Test the Skill

Ask the AI to use your skill:
```
Use the my-skill skill to [task description]
```

## Best Practices

### Keep Skills Concise

- **Under 500 lines**: Main SKILL.md should be concise
- **Progressive disclosure**: Put details in reference.md
- **One level deep**: Link directly from SKILL.md to reference files

### Set Appropriate Freedom Level

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches | Code review guidelines |
| **Medium** (pseudocode/templates) | Preferred pattern with variation | Report generation |
| **Low** (specific scripts) | Fragile operations, consistency critical | Database migrations |

### Use Utility Scripts

Pre-made scripts offer advantages:
- More reliable than generated code
- Save tokens (no code in context)
- Save time (no code generation)
- Ensure consistency

## Common Patterns

### Template Pattern

Provide output format templates:

```markdown
## Report Structure

Use this template:

```markdown
# [Analysis Title]

## Executive Summary
[One-paragraph overview]

## Key Findings
- Finding 1 with data
- Finding 2 with data
```
```

### Examples Pattern

For skills where output quality depends on examples:

```markdown
## Commit Message Format

**Example 1:**
Input: Added user authentication
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation
```

**Example 2:**
Input: Fixed date display bug
Output:
```
fix(reports): correct date formatting

Use UTC timestamps consistently
```
```

### Workflow Pattern

Break complex operations into clear steps:

```markdown
## Form Filling Workflow

1. Analyze the form
2. Create field mapping
3. Validate mapping
4. Fill the form
5. Verify output
```

## Anti-Patterns to Avoid

### 1. Windows-Style Paths
- ✅ Use: `scripts/helper.py`
- ❌ Avoid: `scripts\helper.py`

### 2. Too Many Options
- ✅ Good: "Use pdfplumber for text extraction. For scanned PDFs, use pdf2image with pytesseract."
- ❌ Bad: "You can use pypdf, or pdfplumber, or PyMuPDF, or..."

### 3. Time-Sensitive Information
- ✅ Good: Use "current method" and "legacy patterns" sections
- ❌ Bad: "If you're doing this before August 2025, use the old API."

### 4. Vague Skill Names
- ✅ Good: `database-analysis`, `code-review`
- ❌ Avoid: `helper`, `utils`, `tools`

## Troubleshooting

### Skill Not Being Applied

- Check description includes trigger terms
- Verify description is in third person
- Ensure skill is in correct location (`~/.cursor/skills/`)
- Test by explicitly asking to use the skill

### Skill Too Verbose

- Move details to `reference.md`
- Keep SKILL.md under 500 lines
- Use progressive disclosure
- Remove redundant explanations

## Related Documentation

- Rules: `~/.cursor/.cursor/README.md`
- Optimization Guide: `~/.cursor/OPTIMIZATION_GUIDE.md`
