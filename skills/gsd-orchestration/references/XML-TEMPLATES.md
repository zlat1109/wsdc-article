# XML Task Templates

## Why XML?

XML provides:
- **Structure** for Claude to parse reliably
- **Clarity** on what goes where
- **Executability** - another Claude instance can follow exactly
- **Extensibility** - easy to add new fields

## Basic Task Template

```xml
<task type="auto">
  <name>[Brief descriptive name]</name>
  <files>[Comma-separated file paths]</files>
  <action>
    [Precise instructions. Include:
    - Specific libraries to use (with versions if critical)
    - Patterns to follow (reference existing code if applicable)
    - Decisions already made in CONTEXT.md
    - Edge cases and how to handle them]
  </action>
  <verify>[Command to verify success]</verify>
  <expected>[Expected output/behavior]</expected>
</task>
```

## Task Template with Parallel Execution Support

For parallel execution, add `id`, `depends`, `inputs`, and `outputs` attributes:

```xml
<task type="auto" id="task-1">
  <name>[Brief descriptive name]</name>
  <files>[Comma-separated file paths]</files>
  <outputs>[What this task produces - components, functions, files]</outputs>
  <action>
    [Precise instructions...]
  </action>
  <verify>[Command to verify success]</verify>
  <expected>[Expected output/behavior]</expected>
</task>

<task type="auto" id="task-2" depends="task-1">
  <name>[Task that depends on task-1]</name>
  <files>[Files]</files>
  <inputs>[What this task needs from task-1]</inputs>
  <action>
    Use [outputs from task-1].
    [Precise instructions...]
  </action>
  <verify>[Command]</verify>
  <expected>[Expected]</expected>
</task>

<task type="auto" id="task-3">
  <!-- No depends = independent, can run parallel with task-2 -->
  <name>[Independent task]</name>
  <files>[Files]</files>
  <action>[Instructions...]</action>
  <verify>[Command]</verify>
  <expected>[Expected]</expected>
</task>
```

### Parallel Execution Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | For parallel | Unique task identifier (task-1, task-2, etc.) |
| `depends` | No | Comma-separated list of task IDs this depends on |
| `inputs` | No | What this task needs from dependencies |
| `outputs` | No | What this task produces for others |

### Dependency Graph Example

```xml
<!-- PLAN-1.md -->
<task type="auto" id="task-1">
  <name>Create base components</name>
  <files>src/components/Button.tsx, src/components/Card.tsx</files>
  <outputs>Button, Card components with Tailwind styling</outputs>
  <action>
    Create reusable Button and Card components.
    Use Tailwind CSS classes.
    Export from src/components/index.ts
  </action>
  <verify>npm run type-check</verify>
  <expected>No type errors, components exported</expected>
</task>

<!-- PLAN-2.md -->
<task type="auto" id="task-2" depends="task-1">
  <name>Create Hero section</name>
  <files>src/sections/Hero.tsx</files>
  <inputs>Button component from task-1</inputs>
  <action>
    Import Button from src/components.
    Create Hero section with headline, subheadline, and CTA button.
  </action>
  <verify>npm run dev, check /</verify>
  <expected>Hero renders with working CTA button</expected>
</task>

<!-- PLAN-3.md -->
<task type="auto" id="task-3">
  <!-- No depends - runs parallel with task-2 -->
  <name>Create Footer section</name>
  <files>src/sections/Footer.tsx</files>
  <action>
    Create Footer with links and copyright.
    No dependencies on other tasks.
  </action>
  <verify>npm run type-check</verify>
  <expected>Footer component renders</expected>
</task>

<!-- PLAN-4.md -->
<task type="auto" id="task-4" depends="task-2,task-3">
  <name>Integration and layout</name>
  <files>src/app/page.tsx</files>
  <inputs>Hero from task-2, Footer from task-3</inputs>
  <action>
    Import Hero and Footer.
    Assemble full page layout.
    Add responsive container.
  </action>
  <verify>npm run build</verify>
  <expected>Build succeeds, page renders all sections</expected>
</task>
```

This creates the dependency graph:
```
task-1 (Base components)
   │
   ├──→ task-2 (Hero)  ──┐
   │                     │
   └──→ task-3 (Footer) ─┴──→ task-4 (Integration)

Execution groups:
  Group 1: [task-1]        Sequential (foundation)
  Group 2: [task-2, task-3] Parallel! (independent)
  Group 3: [task-4]        Sequential (aggregation)
```

---

## Task Types

### Type: auto
Fully automated task - no human input needed.

```xml
<task type="auto">
  <name>Create database schema for users</name>
  <files>migrations/001_create_users.sql, src/db/schema.ts</files>
  <action>
    Create users table with:
    - id (UUID, primary key)
    - email (string, unique, not null)
    - password_hash (string, not null)
    - created_at (timestamp, default now)

    Use Drizzle ORM schema definition in schema.ts.
    Follow existing pattern from posts table.
  </action>
  <verify>psql -d mydb -f migrations/001_create_users.sql</verify>
  <expected>Table created successfully, no errors</expected>
</task>
```

### Type: human-verify
Requires human to check result (UI, UX, visual design).

```xml
<task type="human-verify">
  <name>Implement dashboard layout</name>
  <files>src/pages/dashboard.tsx, src/styles/dashboard.module.css</files>
  <action>
    Create dashboard with:
    - Header: Logo + user menu
    - Sidebar: Navigation links
    - Main: Grid layout (3 columns on desktop, 1 on mobile)
    - Use Tailwind for responsive design

    Follow the wireframe in docs/wireframes/dashboard.png
  </action>
  <verify>npm run dev, navigate to http://localhost:3000/dashboard</verify>
  <expected>Layout matches wireframe, responsive on mobile</expected>
  <human-check>Confirm visual design matches expectations, spacing looks good</human-check>
</task>
```

### Type: research
Research task - investigate and document findings.

```xml
<task type="research">
  <name>Research state management options</name>
  <files>.gsd/phases/phase-2/RESEARCH.md</files>
  <action>
    Investigate state management for Next.js 14 app:
    - Zustand vs Jotai vs Redux Toolkit
    - Bundle size impact
    - TypeScript support
    - Persistence options

    Create comparison table in RESEARCH.md
  </action>
  <verify>cat .gsd/phases/phase-2/RESEARCH.md</verify>
  <expected>Markdown table with recommendations</expected>
</task>
```

---

## Task With Dependencies

```xml
<task type="auto" depends="task-1">
  <name>Add form validation</name>
  <files>src/components/LoginForm.tsx</files>
  <action>
    Use zod for schema validation.
    Import the User type from task-1 (src/types/user.ts).

    Validation rules:
    - email: valid email format
    - password: min 8 chars, at least one number

    Show inline errors below each field (red text).
    Disable submit button while validating.
  </action>
  <verify>npm test -- LoginForm.test.tsx</verify>
  <expected>All validation tests pass (8 tests)</expected>
</task>
```

The `depends="task-1"` attribute means this task MUST run after task-1.

---

## Complex Example: API Endpoint

```xml
<task type="auto">
  <name>Create POST /api/articles endpoint</name>
  <files>src/app/api/articles/route.ts, src/lib/db/articles.ts</files>
  <action>
    Implement POST handler for creating articles.

    Libraries:
    - Use Zod for request validation
    - Use Drizzle ORM for database insert
    - Use jose for JWT verification (not jsonwebtoken)

    Request body:
    {
      "title": string (required, 5-200 chars),
      "content": string (required, 10-50000 chars),
      "tags": string[] (optional, max 5 tags)
    }

    Flow:
    1. Verify JWT from cookie
    2. Validate request body with Zod
    3. Insert into articles table with user_id from JWT
    4. Return created article with id

    Error handling:
    - No JWT → 401 {"error": "Unauthorized"}
    - Invalid body → 400 {"error": "Validation failed", "details": [...]}
    - DB error → 500 {"error": "Internal server error"}

    Edge cases:
    - Empty title → Validation error
    - Duplicate title (same user) → Allow (no unique constraint)
    - Very long content → Validation caps at 50k chars
  </action>
  <verify>
    # Test success case
    curl -X POST http://localhost:3000/api/articles \
      -H "Content-Type: application/json" \
      -H "Cookie: auth_token=..." \
      -d '{"title":"Test Article","content":"This is content"}'

    # Test validation error
    curl -X POST http://localhost:3000/api/articles \
      -H "Content-Type: application/json" \
      -H "Cookie: auth_token=..." \
      -d '{"title":"AB"}'
  </verify>
  <expected>
    Success: 201 + {"id":"...","title":"Test Article",...}
    Validation error: 400 + {"error":"Validation failed","details":[...]}
  </expected>
</task>
```

---

## Complex Example: UI Component

```xml
<task type="human-verify">
  <name>Create ArticleCard component</name>
  <files>src/components/ArticleCard.tsx, src/components/ArticleCard.test.tsx</files>
  <action>
    Create reusable ArticleCard component with TypeScript.

    Props interface:
    interface ArticleCardProps {
      article: {
        id: string
        title: string
        excerpt: string
        author: string
        publishedAt: string
        tags: string[]
      }
      onDelete?: () => void
      variant?: 'compact' | 'full'
    }

    Variant: compact
    - Title (h3, truncate at 60 chars)
    - Excerpt (p, truncate at 120 chars)
    - Author + date (small text)
    - Tags (max 3 visible, "+ N more" if more)

    Variant: full
    - Same as compact but no truncation
    - Delete button (if onDelete provided)

    Styling:
    - Use Tailwind CSS
    - Card: bg-white, rounded-lg, shadow, p-4
    - Hover: shadow-lg transition
    - Tags: pill shape, different colors per tag

    Tests:
    - Renders correctly in compact mode
    - Renders correctly in full mode
    - Truncates long text in compact mode
    - Shows delete button when onDelete provided
    - Calls onDelete when button clicked
  </action>
  <verify>
    npm test -- ArticleCard.test.tsx
    npm run dev (visual check at /articles page)
  </verify>
  <expected>
    Tests: 5/5 pass
    Visual: Card displays correctly, hover effect works
  </expected>
  <human-check>
    - Typography looks good (font sizes, spacing)
    - Colors match design system
    - Hover effect feels smooth
    - Mobile responsive (check at 375px width)
  </human-check>
</task>
```

---

## Complex Example: Database Migration

```xml
<task type="auto">
  <name>Add full-text search to articles</name>
  <files>
    migrations/003_add_article_search.sql,
    src/lib/db/search.ts,
    src/app/api/search/route.ts
  </files>
  <action>
    Add full-text search capability for articles.

    Migration (PostgreSQL):
    - Add tsvector column: search_vector
    - Create GIN index on search_vector
    - Create trigger to auto-update search_vector
    - Update existing rows

    Search function (search.ts):
    - Function: searchArticles(query: string, limit: number)
    - Use ts_query for search
    - Rank results by ts_rank
    - Return array of articles with match score

    API endpoint (route.ts):
    - GET /api/search?q=[query]&limit=[10-100]
    - Validate query (min 2 chars)
    - Call searchArticles
    - Return results with highlighting

    Performance:
    - Index should make search < 50ms for 100k articles
    - Limit results to max 100

    Edge cases:
    - Empty query → 400 "Query required"
    - Special chars in query → Sanitize for ts_query
    - No results → 200 + []
  </action>
  <verify>
    # Run migration
    psql -d mydb -f migrations/003_add_article_search.sql

    # Test search
    curl "http://localhost:3000/api/search?q=typescript&limit=10"

    # Check performance
    psql -d mydb -c "EXPLAIN ANALYZE SELECT * FROM articles WHERE search_vector @@ to_tsquery('test');"
  </verify>
  <expected>
    Migration: No errors, index created
    Search: Returns relevant results in < 100ms
    Performance: Using index (no seq scan)
  </expected>
</task>
```

---

## Commit Message Format

After completing each task, commit with this format:

```
type(phase-N): brief description

- Detail 1
- Detail 2
- Detail 3

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types

- **feat**: New feature
  ```
  feat(phase-2): add user profile editing

  - Implement PUT /api/profile endpoint
  - Add ProfileEditForm component
  - Add validation with Zod

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

- **fix**: Bug fix
  ```
  fix(phase-3): resolve login redirect loop

  - Check for existing session before redirect
  - Clear session on logout properly

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

- **refactor**: Code restructuring, no behavior change
  ```
  refactor(phase-1): extract auth logic to separate module

  - Move JWT functions to lib/auth.ts
  - Update imports across codebase

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

- **test**: Adding/updating tests
  ```
  test(phase-2): add edge case tests for article creation

  - Test empty title validation
  - Test max content length
  - Test duplicate handling

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

- **docs**: Documentation only
  ```
  docs(phase-1): add API documentation for auth endpoints

  - Document POST /api/auth/login
  - Document POST /api/auth/logout
  - Add example requests

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

- **chore**: Maintenance (deps, config, etc.)
  ```
  chore(phase-1): update dependencies

  - Update next to 14.2.0
  - Update react to 18.3.0
  - Update typescript to 5.4.0

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

---

## Planning Depth: Adaptive Examples

### Quick (Minimal) - For Experienced Devs

```xml
<task type="auto">
  <name>Add logout button</name>
  <files>src/components/Header.tsx</files>
  <action>
    Add logout button to header.
    Call POST /api/auth/logout on click.
    Redirect to /login after success.
  </action>
  <verify>Click logout button</verify>
  <expected>Redirects to /login, session cleared</expected>
</task>
```

### Standard (Recommended)

```xml
<task type="auto">
  <name>Add logout functionality</name>
  <files>
    src/components/Header.tsx,
    src/app/api/auth/logout/route.ts
  </files>
  <action>
    1. Create logout endpoint:
       - Clear auth cookie
       - Return 200 {"success": true}

    2. Add logout button to Header:
       - Position: top-right, next to user menu
       - On click: POST to /api/auth/logout
       - On success: redirect to /login
       - On error: show toast notification

    Use existing Button component.
    Follow auth flow from login implementation.
  </action>
  <verify>
    curl -X POST http://localhost:3000/api/auth/logout -H "Cookie: auth_token=..."
  </verify>
  <expected>
    Cookie cleared, 200 response, redirect to /login works
  </expected>
</task>
```

### Comprehensive (Complex Projects)

```xml
<task type="auto">
  <name>Implement secure logout functionality</name>
  <files>
    src/components/Header.tsx,
    src/app/api/auth/logout/route.ts,
    src/lib/session.ts,
    tests/auth.test.ts
  </files>
  <action>
    Implement logout with session invalidation.

    Backend (route.ts):
    1. Verify current session from cookie
    2. If valid session:
       - Add session ID to blocklist (Redis key: "blocklist:[session_id]", TTL: token expiry)
       - Clear auth cookie (httpOnly, secure, sameSite: strict)
       - Return 200 {"success": true}
    3. If no session:
       - Still clear cookie (defensive)
       - Return 200 {"success": true}

    Session utils (session.ts):
    - Add function: addToBlocklist(sessionId: string, expirySeconds: number)
    - Update verifySession to check blocklist
    - Use ioredis for Redis connection

    Frontend (Header.tsx):
    - Add logout button:
      - Icon: LogOut from lucide-react
      - Position: Inside UserMenu dropdown
      - Label: "Sign out"
    - On click:
      - Show loading state (disable button)
      - POST to /api/auth/logout
      - On success: redirect to /login with success message
      - On error: Show error toast, re-enable button
    - Keyboard accessible (Enter to trigger)

    Error handling:
    - Network error → Show "Connection failed, try again" toast
    - Server error → Show "Logout failed, please refresh page"
    - Redis unavailable → Log error but still clear cookie (fail safe)

    Tests (auth.test.ts):
    - Logout with valid session clears cookie
    - Logout adds session to blocklist
    - Blocklisted session cannot access protected routes
    - Multiple logouts don't throw errors
    - Logout works even if Redis is down

    Edge cases:
    - Expired session → Still clear cookie, no error
    - Already logged out → Idempotent, no error
    - Concurrent logouts → Redis handles atomically
  </action>
  <verify>
    # Test logout flow
    npm test -- auth.test.ts

    # Manual test
    1. Login to account
    2. Click logout in user menu
    3. Verify redirect to /login
    4. Try accessing /dashboard (should redirect to /login)
    5. Check Redis for blocklist entry: redis-cli GET blocklist:[session_id]
  </verify>
  <expected>
    - Tests: 5/5 pass
    - Cookie cleared (check DevTools → Application → Cookies)
    - Session in Redis blocklist
    - Cannot access protected routes after logout
    - Logout button shows loading state during request
  </expected>
</task>
```

---

## Best Practices

1. **Be specific** - Name exact libraries, functions, patterns
2. **Reference existing code** - "Follow pattern from login.ts"
3. **Include edge cases** - What happens when X fails?
4. **Make it executable** - Another Claude can implement without asking questions
5. **Verification is specific** - Exact commands, expected outputs
6. **Keep tasks atomic** - One task = one concern
7. **Use dependencies** - Link tasks that must run in order

---

## Common Mistakes

❌ **Vague actions**
```xml
<action>Add authentication</action>
```

✅ **Specific actions**
```xml
<action>
Use jose for JWT. Create /api/auth/login endpoint.
Validate credentials against users table. Return httpOnly cookie.
</action>
```

❌ **No verification**
```xml
<verify>Test it manually</verify>
```

✅ **Specific verification**
```xml
<verify>
curl -X POST localhost:3000/api/auth/login \
  -d '{"email":"test@test.com","password":"pass123"}'
</verify>
<expected>200 + Set-Cookie header</expected>
```

❌ **Missing edge cases**
```xml
<action>Create login form</action>
```

✅ **Edge cases included**
```xml
<action>
Create login form.
Edge cases:
- Empty fields → Show "Required" error
- Invalid email → Show "Invalid format"
- Network error → Show retry button
</action>
```

---

## Agent Project Task Templates

When a phase uses ARCHITECTURE.md from agent-architect, use these specialized templates for agent system implementation.

### Agent Implementation Task

```xml
<task type="auto">
  <name>Implement agent definitions and prompts</name>
  <files>
    agents/definitions.py,
    prompts/main_agent.md,
    prompts/[agent_name].md (per ARCHITECTURE.md)
  </files>
  <action>
    Create agent prompt files as markdown in prompts/ directory.
    Each agent from ARCHITECTURE.md gets its own prompt file containing
    the Identity (Role/Goal/Backstory) as system prompt text.

    Implement AgentDefinition instances per ARCHITECTURE.md:
    - description: What the orchestrator sees
    - prompt: Loaded from prompts/*.md at runtime
    - tools: As specified in ARCHITECTURE.md

    Include Task Dispatch Templates in the orchestrator prompt:
    - Process, Input Format, Guidelines, Output Format per agent

    Use load_prompt() helper to read markdown files at runtime.
  </action>
  <verify>python -c "from agents.definitions import agents; print(len(agents))"</verify>
  <expected>Agent count matches ARCHITECTURE.md, all prompt files exist</expected>
</task>
```

### Tools + MCP Setup Task

```xml
<task type="auto">
  <name>Implement tools and MCP server configuration</name>
  <files>
    tools/custom_tools.py,
    main.py (mcp_servers config),
    .env
  </files>
  <action>
    Implement custom MCP tools per ARCHITECTURE.md tools section:
    - Use @tool decorator for each custom tool
    - Create MCP server with create_sdk_mcp_server()

    Configure external MCP servers per ARCHITECTURE.md:
    - Add mcp_servers dict to ClaudeAgentOptions
    - Add mcp_<server>_* to allowed_tools (wildcard pattern)
    - Add required environment variables to .env

    If output destination is MCP-based:
    - Configure the output MCP server (e.g., Notion, Slack)
    - Test connection and tool availability

    CRITICAL: Ensure ALL tools (subagent + MCP) are in allowed_tools.
    Read-only tools (Read, Grep, Glob) are default — don't list them.
  </action>
  <verify>
    python -c "from tools.custom_tools import tools_server; print('OK')"
    # Verify MCP connection
    python -c "import os; assert os.getenv('NOTION_TOKEN'), 'Missing token'"
  </verify>
  <expected>Custom tools created, MCP servers configured, env vars set</expected>
</task>
```

### Orchestration + Integration Task

```xml
<task type="auto" depends="task-1,task-2">
  <name>Implement orchestration, skill, and interaction loop</name>
  <files>
    main.py,
    .claude/skills/[skill-name]/SKILL.md (if guiding skill)
  </files>
  <action>
    Wire everything together per ARCHITECTURE.md orchestration section:

    1. Main agent setup (ClaudeAgentOptions):
       - system_prompt from prompts/main_agent.md
       - agents= dict with all AgentDefinition instances
       - mcp_servers= with configured servers
       - allowed_tools= with ALL tools (direct + subagent + MCP + Task + Skill)
       - setting_sources=["user", "project"] (if using skills)

    2. Orchestration pattern:
       - Single: Direct query()
       - Pipeline: Sequential query() calls with context passing
       - Orchestrator: Main agent dispatches via Task tool
       - Parallel: asyncio.gather() for independent subagents

    3. Guiding skill (if specified in ARCHITECTURE.md):
       - Create SKILL.md with workflow phases
       - Reference additional .md files for detailed specs

    4. Interaction mode (per ARCHITECTURE.md):
       - One-shot: Single query()
       - Conversational: while loop with input() + query()
       - Plan-first: Show plan, wait for approval, then execute

    5. Tool confirmation (if required by ARCHITECTURE.md):
       - Implement permission prompt for destructive tools
  </action>
  <verify>
    # Run agent with test prompt
    echo "test" | python main.py
  </verify>
  <expected>
    Agent starts, dispatches subagents correctly,
    produces output in expected format, writes to output destination
  </expected>
</task>
```

### Key Principles for Agent Tasks

1. **Prompts as files** — Store all prompts in `prompts/*.md`, never hardcode
2. **allowed_tools completeness** — Every tool any subagent uses MUST be in allowed_tools
3. **Fresh context per task** — Don't carry implementation details across tasks
4. **ARCHITECTURE.md as source of truth** — Reference specific sections, not the whole file
5. **Test integration last** — Task 3 depends on Task 1 and Task 2

---

## ML/DL Domain Task Templates

When CONTEXT.md contains ML/DL domain decisions (detected via `ml-dl-skills` integration), use these specialized templates. Each includes a `<domain-skill>` tag declaring which sub-skill the executor should consult.

### ML Data Preparation Task

```xml
<task type="auto">
  <name>Data preparation and splitting</name>
  <domain-skill>ml-fundamentals, data-pipeline</domain-skill>
  <files>src/data/prepare.py, src/data/transforms.py</files>
  <action>
    Follow ml-fundamentals data preparation patterns:
    1. EDA: df.shape, df.info(), class distribution, missing values
    2. Split FIRST: train_test_split(stratify=y) — 80/10/10
    3. Preprocess: fit scaler on train ONLY, transform all sets
    4. Save: processed datasets + fitted transformers

    CRITICAL: Never fit any transformer on test/val data!
    Set random seeds: np.random.seed(42), torch.manual_seed(42)
  </action>
  <verify>python -m pytest tests/test_data.py -v</verify>
  <expected>Data splits correct, shapes verified, no leakage</expected>
</task>
```

### ML Model Training Task

```xml
<task type="auto" depends="task-1">
  <name>Model architecture and training</name>
  <domain-skill>pytorch-mastery, deep-learning-core</domain-skill>
  <files>src/models/model.py, src/training/train.py</files>
  <action>
    Follow pytorch-mastery training loop pattern:
    1. Model: nn.Module, match output dims to task
    2. Loss: BCEWithLogitsLoss (binary) / CrossEntropyLoss (multiclass)
    3. Optimizer: Adam/AdamW, scheduler: ReduceLROnPlateau
    4. Loop: model.train() for train, model.eval()+no_grad() for val
    5. Early stopping, save best checkpoint

    CRITICAL: BCEWithLogitsLoss (NOT BCELoss). Always eval mode for validation.
  </action>
  <verify>python src/training/train.py --epochs 2 --dry-run</verify>
  <expected>Training completes, val metrics computed, checkpoint saved</expected>
</task>
```

### ML Evaluation Task

```xml
<task type="auto" depends="task-2">
  <name>Model evaluation and analysis</name>
  <domain-skill>model-interpretability, ml-fundamentals</domain-skill>
  <files>src/evaluation/evaluate.py, src/evaluation/report.py</files>
  <action>
    Follow model-interpretability evaluation patterns:
    1. Metrics: accuracy, F1, confusion matrix, ROC-AUC (classification)
       or MSE, MAE, R² (regression)
    2. Error analysis: worst predictions, systematic biases
    3. Baseline comparison: random, majority class, simple model
    4. Interpretability: SHAP / Grad-CAM / attention weights
    5. Generate evaluation report

    Compare ALL metrics against baseline — never report without context.
  </action>
  <verify>python src/evaluation/evaluate.py --model checkpoints/best.pt</verify>
  <expected>Report generated, metrics above baseline, no anomalies</expected>
</task>
```

### RAG System Task

```xml
<task type="auto">
  <name>Build RAG pipeline</name>
  <domain-skill>rag-retrieval, data-pipeline, transformers-llm</domain-skill>
  <files>src/rag/pipeline.py, src/rag/embeddings.py, src/rag/retriever.py</files>
  <action>
    Follow rag-retrieval RAG architecture pattern:
    1. Document loading: PDF/text parsing via data-pipeline patterns
    2. Chunking: recursive text splitter, 500-1000 tokens, 10-20% overlap
    3. Embeddings: sentence-transformers or OpenAI embeddings
    4. Vector store: FAISS (local) or ChromaDB (persistent)
    5. Retrieval: top-k similarity search with score threshold
    6. Generation: LLM with retrieved context in prompt

    Evaluate: faithfulness, relevance, answer completeness
  </action>
  <verify>python src/rag/pipeline.py --test-query "sample question"</verify>
  <expected>Answer generated with source citations, retrieval scores logged</expected>
</task>
```

### ML/DL Verification Template

Use this verification output format for `gsd verify` on ML/DL phases:

```markdown
### ML/DL Domain Checks
[✓ / ✗] Data split before preprocessing (no leakage)
[✓ / ✗] Scaler/encoder fit on train ONLY
[✓ / ✗] Correct loss function for task type
[✓ / ✗] model.eval() + torch.no_grad() for inference
[✓ / ✗] Random seeds set for reproducibility
[✓ / ✗] No augmentation/SMOTE on test data
[✓ / ✗] Metrics compared against baseline
[✓ / ✗] Class imbalance handled (if applicable)
[✓ / ✗] Training curves show convergence
[✓ / ✗] Best checkpoint saved
```
