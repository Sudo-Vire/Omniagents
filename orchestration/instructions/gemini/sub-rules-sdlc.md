# SDLC & Comprehensive Workflow Guidelines (Modular Subfile)

## 3. Standard Workflow and Execution Methodology (Mandatory for All Tasks)
This section defines exactly the step-by-step process the assistant must follow in all interactions, prompts, refactorizations, reviews, or code development.

### 3.1 Phase 0 – Mandatory Decision Tree (First Step – Always Execute)
Before doing anything else, the assistant must decide the complexity of the task:
- **Simple Task** (use Simplified Flow – section 3.8): Correction of a single line/error, direct query, refactoring < 10 lines, small comment.
- **Complex Task** (use Full Workflow – sections 3.2 to 3.7): Medium/large refactoring, new feature/component/endpoint, architecture, UI/UX, security, testing, multi-file changes.
- **Rule**: If in doubt, treat the task as Complex.

### 3.2 Phase 1 – Mandatory Skill and Tool Invocation (Mandatory)
Before writing a single line of code or giving any technical response, execute in this order:
1. Invoke the `skill` tool corresponding to the task domain.
2. If the task touches architecture, repository structure, or queries like “how do I…”, “where is…”, “what does…” -> immediately execute `graphify query "<question>"` and review ARCHITECTURE.md.
3. If the task has security risks -> invoke Strix or the security agent.

### 3.3 Phase 2 – Catalog and Agent Selection (Mandatory)
- **Use the macro catalog** (`agency-agents`) when the task requires main engineering, architecture, backend/frontend, UI/UX, cybersecurity, product, marketing, etc.
- **Use the granular tactical catalog** (`claude-subagents`) when very specific technical specialization in a language or framework is needed.

### 3.4 Phase 3 – Execution with Virtual Office and Aider (Mandatory for complex tasks)
1. **Virtual Office**: Generates detailed plan/report in OFFICE_RESULT.md. Never generates massive code.
2. **Aider**: Takes OFFICE_RESULT.md context and writes, refactors, corrects, and commits the actual code.

### 3.5 Phase 4 – Validation and Verification (Mandatory)
1. **Linting & Formatting**: Python -> `ruff check` + `ruff format`, Web -> `biome check`.
2. **Visual Validation (UI)**: Use Browser-Use or native tools (`openBrowserPage`, `readPage`).
3. **Regression Verification**: Check existing behavior is not broken.
4. **Security**: Review against OWASP Top 10, run Strix.

### 3.6 Phase 5 – Git Workflow (Mandatory)
Apply Complete Git Standard: branch naming (`feature/`, `bugfix/`, `hotfix/`, `refactor/`, `docs/`), Conventional Commits (`type(scope): description`), SemVer tags.

### 3.7 Phase 6 – Cleanup and Closure (Mandatory)
1. Remove temporary files.
2. Save session results exclusively in `session-state/files/`.
3. Absolute Markdown links and documentation check.

### 3.8 Simplified Flow (YAGNI + Immediate Action) – For Small Tasks
Analyze with YAGNI -> Minimal surgical change -> Linters -> Visual validation -> Conventional commit -> Close.

### 3.9 Golden Rules (Never skip)
- Never skip Phase 1 on complex tasks.
- Always use absolute Markdown links.
- Always perform visual validation of UI changes.
- Never leave test files in root.

## 5. SDLC – Software Development Life Cycle (General Cycle)
Every task follows 8 phases (Requirements & Planning, Design, Development & Implementation, Security & Compliance, Testing & QA, Git Workflow, Deployment/Cloudflare, Maintenance & Research). In each SDLC phase, the assistant must:
1. Think out loud.
2. Present the plan.
3. Ask for explicit confirmation: "Is this correct or would you like to make any changes?"
4. Wait for explicit user approval before proceeding.
