# Standard Workflow and Execution Methodology (Modular Subfile)

## 1. Standard Workflow and Execution Methodology (Mandatory for All Tasks)

### 1.1 Phase 0 – Mandatory Decision Tree (First Step – Always Execute)
**Before doing anything else**, the assistant must decide the complexity of the task:
- **Simple Task** (use Simplified Flow – section 1.8):
  - Correction of a single line or obvious error.
  - Direct query (“where is…?”, “what does…”).
  - Refactoring of less than 10 lines.
  - Adding a small comment or minor improvement.
- **Complex Task** (use Full Workflow – sections 1.2 to 1.7):
  - Any medium or large refactoring.
  - Adding new functionality, component, or endpoint.
  - Changes involving architecture, UI/UX, security, testing, or multiple files.
**Rule**: If in doubt, treat the task as **Complex**.

### 1.2 Phase 1 – Mandatory Skill and Tool Invocation (Mandatory)
**Before writing a single line of code or giving any technical response**, execute in this order:
1. Invoke the `skill` tool corresponding to the task domain.
2. If the task touches architecture, repository structure, or queries like “how do I…”, “where is…”, “what does…” → immediately execute:
   - `graphify query "<question>"`
   - Review [ARCHITECTURE.md](./ARCHITECTURE.md)
3. If the task has security risks → invoke Strix or the security agent.

### 1.3 Phase 2 – Catalog and Agent Selection (Mandatory)
- **Use the macro catalog** (`agency-agents`) when the task requires main engineering, architecture, backend/frontend, UI/UX, cybersecurity, product, marketing, etc.
- **Use the granular tactical catalog** (`claude-subagents`) when very specific technical specialization in a language or framework is needed.
- **Synergy decision**: CrewAI can use macro roles and enrich them with tactical micro-agents.
**Mandatory work structure**: **Area → Exact Agent/Sub-agent → Main Tool → Detailed Flow**

### 1.4 Phase 3 – Execution with Virtual Office and Aider (Mandatory for complex tasks)
1. **Virtual Office**:
   - Generates the detailed plan or report in `OFFICE_RESULT.md`.
   - Includes technical decisions, modular structure, requirements, aesthetics, etc.
   - **Never** generates massive code (except in very small tasks).
2. **Aider**:
   - Takes the content of `OFFICE_RESULT.md` as context.
   - Writes, refactors, corrects, and commits the actual code in the repository.

### 1.5 Phase 4 – Validation and Verification (Mandatory)
After any code or interface change:
1. **Linting and Formatting** (mandatory): Python (`ruff check` + `ruff format`), JS/TS/Web (`biome check`).
2. **Visual Validation (UI)**: Use **Browser-Use** or native tools (`openBrowserPage`, `readPage`, etc.).
3. **Regression Verification**: Check that existing behavior is not broken; run relevant tests.
4. **Security**: Review against OWASP Top 10; run Strix if the task touches endpoints or auth.

### 1.6 Phase 5 – Git Workflow (Mandatory)
Apply Complete Git Standard: correct branch naming, Conventional Commits, changelog with `git-cliff`.

### 1.7 Phase 6 – Cleanup and Closure (Mandatory)
1. Remove all temporary files and single-use scripts.
2. Save session results exclusively in `session-state/files/`.
3. Confirm absolute Markdown links.
4. Confirm documentation is updated.

### 1.8 Simplified Flow (YAGNI + Immediate Action) – For Small Tasks
1. Analyze problem with YAGNI.
2. Propose or write minimal/surgical change.
3. Apply linters (`ruff` / `biome`).
4. Visual validation if UI.
5. Commit with Conventional Commit.
6. Clean and close.

### 1.9 Golden Rules (Never skip)
- **Never** skip Phase 1 when task is complex.
- **Always** use absolute Markdown links.
- **Always** perform visual validation of UI changes.
- **Never** leave test files in root.
- **Always** follow full flow for complex tasks.
- **Always** decide complexity in Phase 0.

---

## 2. SDLC – Software Development Life Cycle (General Cycle)
Every task follows these 8 phases. In each phase the assistant must:
1. Think out loud.
2. Present the plan.
3. Ask explicit confirmation: **“Is this correct or would you like to make any changes?”**
4. Wait for explicit user approval before proceeding.

- **Phase 1 – Requirements & Planning** (`product/`, `project-management/`, superpowers, Karpathy).
- **Phase 2 – Design** (`design/`, `engineering/`).
- **Phase 3 – Development & Implementation** (relevant engineering agents).
- **Phase 4 – Security & Compliance** (`security/`, `healthcare/`, Strix).
- **Phase 5 – Testing & Quality Assurance** (`testing/`, `academic/`, Browser-Use).
- **Phase 6 – Git Workflow & Version Control** (branching, Conventional Commits).
- **Phase 7 – Deployment & DevOps** (Cloudflare / Wrangler).
- **Phase 8 – Maintenance, Support & Research** (incident resolution, support, research).
