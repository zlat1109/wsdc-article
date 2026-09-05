---
name: cursor-orchestration
description: Chooses Cursor Skills, MCP servers, and Rules for multi-domain work (Python, Tableau, web, GitHub). Use when the user asks how to work in Cursor, which tool to use, or to optimize agent workflow across scraping, analytics, and repos.
---

# Cursor orchestration

## Quick decision tree

1. **Need structured decomposition?** → Call **sequential-thinking** MCP (or ask user for phased plan).
2. **Need official docs?** → Skill **documentation-lookup** + **context7** MCP (resolve-library-id → query-docs).
3. **Need GitHub truth?** → **github** MCP.
4. **Need live web search?** → **duckduckgo-search**.
5. **Domain work** → Open the matching **Skill** (`SKILL.md` only first; open `reference/` if needed).

## Skill picker

| User intent | Skill |
|-------------|-------|
| WSDC/Tableau/data viz pipeline | tableau-workflows |
| Scrapers, Telegram, pandas | python-development |
| Static site, CSS, a11y | web-development |
| UI anti-slop (layout, typography) | taste-skill |
| Редизайн существующего сайта/UI | redesign-skill |
| Motion / easing / premium feel | emil-design-eng |
| Tests | testing |
| DB design / SQL | database-analysis |
| Greenfield folder layout | project-setup |
| Обычный PR (bugs, security, tests) | code-review |
| Жёсткий аудит структуры / anti-spaghetti перед merge | thermo-nuclear-code-quality-review |
| Архитектура agent harness (MVP, MCP, permissions) | agents-best-practices |
| Перед новой фичей / библиотекой — поиск готовых решений | search-first |
| Документация API/библиотек (не из training data) | documentation-lookup |
| Статьи, гайды, WSDC long-form | article-writing |
| Голос бренда / автора для статей | brand-voice |
| После фичи: build, tests, smoke, security pass | verification-loop |
| Формальные eval-кейсы / EDD для агента | eval-harness |
| Аудит папок, логов, legacy в workspace | workspace-hygiene-audit |
| Аудит MCP/hooks/skills (harness) | workspace-surface-audit |
| Аудит качества skills | skill-stocktake |
| Мёртвый код внутри одного репо | refactor-clean |
| Job search: оценить JD (Apply/Stretch/Skip) | job-search-role-fit-rater |
| Job search: CV+CL под вакансию | job-search-tailored-resume |
| Job search: убрать AI-tells из CL/CV | job-search-humanize |
| Job search: pipeline / follow-ups | job-search-job-tracker |
| Размытая задача — stress-test плана до кода | grill-me |
| Сложный scope / skill / workflow — интервью до build | process-interviewer |
| Хаотичная мысль → нормальный prompt | prompt-master |
| Убрать AI-slop из любого текста | humanizer |
| LinkedIn — первые 2 строки / hooks | linkedin-hook-generator |
| Проверить факты перед публикацией | fact-checker (+ duckduckgo-search MCP) |
| Не знаю с чего начать проект — план A→Z | gsd-orchestration |
| CV/CL EU/US/UK, ATS, CAR bullets | resume-cover-letter |
| JD match, ATS, interview (ResumeSkills) | job-description-analyzer, resume-tailor, cover-letter-generator, resume-ats-optimizer, resume-bullet-writer, interview-prep-generator, tech-resume-optimizer |

**Frontend stack:** `redesign-skill` (аудит существующего) → `web-development` → `taste-skill` → `emil-design-eng`. Для WSDC-статей: `article-writing` → `fact-checker` → `humanizer`. LinkedIn: `linkedin-hook-generator` → `humanizer`. Impeccable — в project сайта, когда начнёте активный редизайн.

**Content pipeline:** `prompt-master` (если мысли хаотичны) → `grill-me` или `process-interviewer` (если scope неясен) → draft → `fact-checker` → `humanizer`. Job search CV/CL: `job-search-humanize` вместо generic `humanizer`.

## MCP picker

| User intent | MCP |
|-------------|-----|
| Step-by-step reasoning tool | sequential-thinking |
| npm/pip/Tableau API docs | context7 |
| Issues, PRs, file search on GitHub | github |
| Current facts | duckduckgo-search |
| Tableau Cloud REST/metadata | tableau |
| Public Tableau viz | tableau-public |
| Browser automation | Playwright |
| Notion pages | notion |
| Figma | figma |
| md/docx conversion | mcp-pandoc |
| Long-term project memory | memory-bank |

## Hooks awareness

Global **sessionStart** may inject a short tooling reminder; do not repeat it verbatim—act on it.

## Full playbook

See `~/cursor/docs/CURSOR_TOOLING_PLAYBOOK.md` (or workspace `docs/CURSOR_TOOLING_PLAYBOOK.md`).
For ready-to-run prompt templates, use `~/cursor/docs/WORKFLOW_COMMAND_TEMPLATES.md`.

## RPE Review Ship mode

For complex or risky tasks, explicitly follow:
1. **Research** (facts and constraints)
2. **Plan** (phased checkpoints)
3. **Execute** (small reversible changes)
4. **Review** (tests/lints/smoke + secrets check)
5. **Ship** (clear verification summary)

## Gotchas

- Do not load huge reference files unless needed.
- Do not use MCP for everything; prefer local evidence first.
- Keep hooks lightweight; avoid expensive format/lint hooks on every edit.
- Never print secrets from `mcp.json` or token files into chat output.
