# Master Copilot Agent & Skills Instructions (copilot-instructions.md)

This document establishes the permanent, comprehensive, and detailed instructions for the AI assistant in this repository.  
These guidelines must be applied **automatically and mandatorily** in every prompt, interaction, refactoring, review, or code development.

---

## How the Assistant Must Behave (Main Rule)

The assistant **must always** follow this priority order:

1. **Think out loud** before acting.
2. **Present the plan** of the current phase.
3. **Ask for explicit confirmation**:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user approval** before proceeding to the next phase or executing changes.
5. **Execute only after receiving confirmation**.

---

## 1. Local Model Gateway (Omniroute Gateway)
Both the Virtual Office and **Aider** operate natively connected to the local Omniroute gateway:
- **Base Endpoint**: `http://localhost:20128/v1`
- **Model**: use the selected one

- **Purpose**: Ensure high-speed local inference, zero external costs, and absolute privacy of the source code.

---

## 2. Operational Principles and Philosophy ("Ponytail" & Lazy Senior Dev)
- **YAGNI**: The best line of code is the one that never gets written. Minimal, surgical, and direct changes.
- **Action First (ADHD)**: Direct, to-the-point responses. Commands, paths, or code snippets first; explanations later.
- **Reusability > Creation**: Prioritize standard libraries, existing code, and native features before adding new dependencies or abstractions.
- **Root Cause Correction**: Address the root cause of problems, not the symptoms.

---

## 3. Standard Workflow and Execution Methodology (Mandatory for All Tasks)

This section defines **exactly** the step-by-step process the assistant must follow in **all** interactions, prompts, refactorizations, reviews, or code development.  
It is applied **automatically and mandatorily**.

### 3.1 Phase 0 – Mandatory Decision Tree (First Step – Always Execute)

**Before doing anything else**, the assistant must decide the complexity of the task:

- **Simple Task** (use Simplified Flow – section 3.8):
  - Correction of a single line or obvious error.
  - Direct query (“where is…?”, “what does…”).
  - Refactoring of less than 10 lines.
  - Adding a small comment or minor improvement.

- **Complex Task** (use Full Workflow – sections 3.2 to 3.7):
  - Any medium or large refactoring.
  - Adding new functionality, component, or endpoint.
  - Changes involving architecture, UI/UX, security, testing, or multiple files.

**Rule**: If in doubt, treat the task as **Complex**.

### 3.2 Phase 1 – Mandatory Skill and Tool Invocation (Mandatory)

**Before writing a single line of code or giving any technical response**, execute in this order:

1. Invoke the `skill` tool corresponding to the task domain.
2. If the task touches architecture, repository structure, or queries like “how do I…”, “where is…”, “what does…” → immediately execute:
   - `graphify query "<question>"`
   - Review [ARCHITECTURE.md](./ARCHITECTURE.md)
3. If the task has security risks → invoke Strix or the security agent.

### 3.3 Phase 2 – Catalog and Agent Selection (Mandatory)

- **Use the macro catalog** (`agency-agents`) when the task requires main engineering, architecture, backend/frontend, UI/UX, cybersecurity, product, marketing, etc.
- **Use the granular tactical catalog** (`claude-subagents`) when very specific technical specialization in a language or framework is needed (e.g., Angular, Django, Docker, etc.).
- **Synergy decision**: CrewAI can use the macro roles and enrich them with tactical micro-agents.

**Mandatory work structure**:
**Area → Exact Agent/Sub-agent → Main Tool → Detailed Flow**

### 3.4 Phase 3 – Execution with Virtual Office and Aider (Mandatory for complex tasks)

1. **Virtual Office**:
   - Generates the detailed plan or report in `OFFICE_RESULT.md`.
   - Includes technical decisions, modular structure, requirements, aesthetics, etc.
   - **Never** generates massive code (except in very small tasks).

2. **Aider**:
   - Takes the content of `OFFICE_RESULT.md` as context.
   - Writes, refactors, corrects, and commits the actual code in the repository.

### 3.5 Phase 4 – Validation and Verification (Mandatory)

After any code or interface change:

1. **Linting and Formatting** (mandatory):
   - Python → `ruff check` + `ruff format`
   - JavaScript/TypeScript/Web → `biome check`

2. **Visual Validation (UI)** (mandatory for any interface change):
   - Use **Browser-Use** or native tools (`openBrowserPage`, `readPage`, etc.).
   - Verify that the result exactly matches the requirements.

3. **Regression Verification**:
   - Check that existing behavior is not broken.
   - Run relevant tests if they exist.

4. **Security** (if applicable):
   - Review against OWASP Top 10.
   - Run Strix if the task touches endpoints or authentication.

### 3.6 Phase 5 – Git Workflow (Mandatory)

Always apply the **Complete Git Standard** (section 12):
- Create a branch with correct naming.
- Use Conventional Commits.
- Generate a changelog with `git-cliff` if a release is planned.

### 3.7 Phase 6 – Cleanup and Closure (Mandatory)

1. Remove all temporary files and single-use scripts.
2. Save session results exclusively in `session-state/files/`.
3. Confirm that all Markdown links are absolute.
4. Confirm that the change is documented if documentation is required.

### 3.8 Simplified Flow (YAGNI + Immediate Action) – For Small Tasks

1. Analyze the problem with YAGNI.
2. Propose or write the minimal and surgical change.
3. Apply linters (`ruff` or `biome`).
4. Perform visual validation if it is UI.
5. Commit with Conventional Commit message.
6. Clean and close.

### 3.9 Golden Rules (Never skip)

- **Never** skip Phase 1 (skill invocation) when the task is complex.
- **Always** use absolute Markdown links.
- **Always** perform visual validation of any UI change.
- **Never** leave test files in the root.
- **Always** follow the full flow for complex tasks.
- **Always** decide complexity in Phase 0.

---

## 4. Dual Collaboration Ecosystem – Unique Index  
(`agency-agents` + `claude-subagents` + CrewAI + Aider)

**Important Note**: For simple tasks apply **YAGNI + Immediate Action**. For complex tasks combine both catalogs.

**Work structure**: **Area → Agent/Sub-agent → Main Tool → Detailed Flow**

### 4.1 Design and Interface (`design/`)
- **Area**: UI/UX, visual components, animations, accessibility (WCAG), and design systems.
- **Macro Agent**: `design/design-ui-designer.md`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI generates a detailed design report in `OFFICE_RESULT.md`.
  2. The report **does not contain massive code**.
  3. Aider applies the changes directly to the CSS/HTML files in the workspace.

### 4.2 Engineering and Architecture (`engineering/`)
- **Area**: Software architecture, backend, frontend, databases, design patterns, refactorizations.
- **Macro Agent**: `engineering/engineering-software-architect.md` and `engineering/engineering-senior-developer.md`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI designs the modular structure and technical decisions in `OFFICE_RESULT.md`.
  2. Aider writes, refactorizes, and commits the actual code in the repository.

### 4.3 Cybersecurity and Pentesting (`security/` + `Strix`)
- **Area**: OWASP Top 10 and API Security audit, vulnerabilities, penetration testing.
- **Macro Agent**: `security/` (Security Auditor) or `engineering/engineering-identity-access-engineer.md`
- **Main Tool**: **Strix** + Virtual Office + Aider
- **Concrete Flow**:
  1. Strix analyzes the code, detects and exploits vulnerabilities.
  2. CrewAI documents the analysis in `OFFICE_RESULT.md`.
  3. Aider applies the patches safely.

### 4.4 Product and Strategy (`product/`)
- **Area**: Business requirements, scope, user stories, MVP definition.
- **Macro Agent**: `product/product-manager.md`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI structures the requirements and documents them in `OFFICE_RESULT.md`.

### 4.5 Marketing and Content (`marketing/`)
- **Area**: Copywriting, SEO, content strategy, tone of voice.
- **Macro Agent**: `marketing/`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI generates texts in `OFFICE_RESULT.md`.
  2. Aider implements the changes.

### 4.6 Paid Media and Campaigns (`paid-media/`)
- **Area**: Advertising strategy, performance advertising, paid campaigns.
- **Macro Agent**: `paid-media/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI generates advertising strategies in `OFFICE_RESULT.md`.

### 4.7 Finance and FinOps (`finance/`)
- **Area**: Financial modeling, costs, economic optimization, FinOps.
- **Macro Agent**: `finance/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI performs viability and cost analysis in `OFFICE_RESULT.md`.

### 4.8 Game Development (`game-development/`)
- **Area**: Game mechanics, game loops, interactive systems.
- **Macro Agent**: `game-development/`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI designs game loops in `OFFICE_RESULT.md`.
  2. Aider implements the logic.

### 4.9 GIS and Geospatial Data (`gis/`)
- **Area**: Spatial analysis, digital cartography, coordinate processing.
- **Macro Agent**: `gis/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI processes and analyzes geospatial data in `OFFICE_RESULT.md`.

### 4.10 Health and Healthcare (`healthcare/`)
- **Area**: Medical regulatory compliance, health systems, health data privacy.
- **Macro Agent**: `healthcare/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI validates regulatory compliance and documents everything in `OFFICE_RESULT.md`.

### 4.11 Project Management (`project-management/`)
- **Area**: Agile planning, sprints, schedules, dependency management.
- **Macro Agent**: `project-management/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI breaks down milestones, tasks and states in `OFFICE_RESULT.md`.

### 4.12 Research (`research/`)
- **Area**: Web research, data synthesis, competitive intelligence, benchmarks.
- **Macro Agent**: `research/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI generates detailed research reports in `OFFICE_RESULT.md`.

### 4.13 Sales (`sales/`)
- **Area**: Conversion funnels, commercial strategy, sales pipelines.
- **Macro Agent**: `sales/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI optimizes sales processes in `OFFICE_RESULT.md`.

### 4.14 Spatial Computing (`spatial-computing/`)
- **Area**: Immersive AR/VR experiences, mixed reality, 3D environments.
- **Macro Agent**: `spatial-computing/`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI specifies 3D environments in `OFFICE_RESULT.md`.
  2. Aider implements the logic.

### 4.15 Technical Support (`support/`)
- **Area**: Incident resolution, troubleshooting, FAQs.
- **Macro Agent**: `support/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI generates troubleshooting guides in `OFFICE_RESULT.md`.

### 4.16 Testing and QA (`testing/`)
- **Area**: Unit, integration, E2E, automated testing.
- **Macro Agent**: `testing/`
- **Main Tool**: Virtual Office + **Aider** + **Browser-Use**
- **Concrete Flow**:
  1. CrewAI defines test cases in `OFFICE_RESULT.md`.
  2. Aider implements the tests.
  3. Every UI change is verified with **Browser-Use**.

### 4.17 Academic Research (`academic/`)
- **Area**: Statistical analysis, scientific studies, methodological rigor.
- **Macro Agent**: `academic/`
- **Main Tool**: Virtual Office
- **Concrete Flow**:
  - CrewAI elaborates scientific rigor documents in `OFFICE_RESULT.md`.

### 4.18 Specialized Domains (`specialized/`)
- **Area**: Custom workflows and niche cases.
- **Macro Agent**: `specialized/`
- **Main Tool**: Virtual Office + **Aider**
- **Concrete Flow**:
  1. CrewAI designs the specific workflow in `OFFICE_RESULT.md`.
  2. Aider implements the code.

---

## 5. SDLC – Software Development Life Cycle (General Cycle)

The **SDLC** is the general lifecycle followed by the assistant. Every task follows these 8 phases.

**In each SDLC phase the assistant must:**

1. **Think out loud** – Clearly state what it has reasoned and decided in that phase.
2. **Present the plan** – Show the proposed actions for that phase.
3. **Ask for explicit confirmation** – Explicitly ask:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user approval** before proceeding to the next phase or executing changes.

### SDLC Phase 1 – Requirements & Planning (Superpowers + Karpathy Skills)
- **Tasks**: Elicit requirements, create user stories, define MVP, apply `brainstorming`, `writing-plans`, and Karpathy’s principles.
- **Main Agents**: `product/`, `project-management/`, `superpowers`, `multica-ai/andrej-karpathy-skills`
- **Output**: Structured plan in `OFFICE_RESULT.md`

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 2 – Design
- **Tasks**: UI/UX design, accessibility, architecture design.
- **Main Agents**: `design/`, `engineering/`
- **Output**: Design report in `OFFICE_RESULT.md`

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 3 – Development & Implementation
- **Tasks**: Write and integrate code.
- **Main Agents**: Relevant engineering and specialized agents
- **Output**: Working code committed

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 4 – Security & Compliance
- **Tasks**: OWASP audit, penetration testing, compliance checks.
- **Main Agents**: `security/`, `healthcare/`
- **Output**: Security report + patches

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 5 – Testing & Quality Assurance
- **Tasks**: Unit/E2E testing + visual regression with **Browser-Use**.
- **Main Agents**: `testing/`, `academic/`
- **Output**: Validated code

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 6 – Git Workflow & Version Control
- **Tasks**: Branching, Conventional Commits, changelog generation.
- **Output**: Clean Git history + CHANGELOG.md

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 7 – Deployment & DevOps (Cloudflare)
- **Tasks**: Deploy to **Cloudflare**.
- **Tools**: Cloudflare CLI / Wrangler
- **Output**: Production deployment

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

### SDLC Phase 8 – Maintenance, Support & Research
- **Tasks**: Incident resolution, troubleshooting, marketing content, sales funnels, academic research, continuous improvement.
- **Output**: Updated documentation and support materials

**Assistant must do the following before proceeding:**

1. Think out loud about what was decided in this phase.
2. Present the concrete plan for this phase.
3. Ask explicitly:  
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user confirmation** before moving to the next phase or executing changes.

---

## 6. Complete Git Standard (Git Workflow)
For maintaining an impeccable, professional and automatable Git lifecycle and history (especially when Aider or agents manage changes):

1. **Branch Naming (`git branch`)**:
   - `feature/feature-name` (new features)
   - `bugfix/error-description` (bug fixes)
   - `hotfix/critical-description` (urgent production patches)
   - `refactor/module-name` (structural improvements without changing behavior)
   - `docs/documentation-update` (documentation changes)

2. **Commit Messages (Conventional Commits)**:
   - **Mandatory format**: `type(scope): brief imperative description`
   - **Allowed types**: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`, `ci`, `build`

3. **Tagging and Versions (SemVer)**:
   - Strict use of semantic versioning for tags (`vMAJOR.MINOR.PATCH`)

---

## 7. Automated Changelog Generation (Git-Cliff)
- **Tool**: **Git-Cliff** (`git-cliff`)
- **Command**: `git-cliff -o CHANGELOG.md`
- **Purpose**: Automatically generate a professional structured changelog from semantic commit history before publishing a release or tag.

---

## 8. Superpowers (`superpowers`) Framework & SDLC Methodology
- **Location**: `superpowers`
- **Purpose**: Agentic skills framework and software development methodology for structured flows of brainstorming, TDD, systematic debugging, plan writing/execution, and subagent-guided development.
- **Key Skills**: `brainstorming`, `test-driven-development`, `systematic-debugging`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `verification-before-completion`

---

## 9. Andrej Karpathy Skills (`multica-ai/andrej-karpathy-skills`)
- **Location**: `multica-ai/andrej-karpathy-skills`
- **Purpose**: Behavioral guidelines and coding rules based on Andrej Karpathy's observations on LLM coding pitfalls:
  1. **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
  2. **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
  3. **Surgical Changes**: Touch only what you must. Clean up only your own mess.
  4. **Goal-Driven Execution**: Define success criteria. Loop until verified.
- **Integration**: Loaded alongside project instructions to enforce cautious, surgical, and goal-driven LLM coding workflows.

---

## 10. Browser-Use & E2E Autonomous Browser Testing Integration
- **Tool**: **Browser-Use** (`browser-use/browser-use`)
- **Purpose**: AI-driven browser automation for autonomous End-to-End (E2E) testing, graphical interface verification, complex user flows and real-time validation.
- **Mandatory Verification Policy**: Every UI change must be verified autonomously using Browser-Use (or integrated Playwright/MCP tools) before finishing any workflow.

---

## 11. Rules of Automatic Execution and Obligatoriness
1. **Mandatory Skill Invocation**  
   Before starting **any** development, UI/UX, code review, security or architecture task, it is **MANDATORY** to invoke the `skill` tool with the corresponding skill.

2. **Graphify + Architecture**  
   Before modifying any component or responding about the repository structure, it is **MANDATORY** to inspect [ARCHITECTURE.md](./ARCHITECTURE.md) and consult the graph with `graphify query "<question>"`.

3. **Markdown Links**  
   Always use absolute Markdown links for file references (`[name](absolute_path)`).

4. **No Regressions**  
   Validate that changes preserve existing behavior.

5. **Cleaning**  
   Eliminate temporary files at the end of tasks.

---

## 12. Validation and Environment Protocol
1. **Mandatory Visual Validation (UI)**: All visual modifications must be validated with integrated browser tools (`openBrowserPage`, `readPage`, etc.).
2. **PowerShell Commands**: Use native commands (`Get-ChildItem`, etc.) and avoid incompatible operators (`&&`, `||`, etc.).

---

## 13. Robustness and Artifact Management
1. **Defense against Nulls and DOM Failures**: Verify element existence before manipulating them (`if (!container) return;`).
2. **Artifact Management**: No test files in root. Session results exclusively in `session-state/files/`.

---

## 14. Code Review (before approving any change)
- Surgical precision and YAGNI
- Root cause correction
- UI/UX quality + WCAG (contrast ≥ 4.5:1, keyboard navigation, ARIA)
- No regressions
- Correct use of absolute Markdown links
- Security and privacy (no exposed credentials, no OWASP Top 10)
- Compliance with project coding standards

---

## 15. Architectural Knowledge Graph (Graphify)
For any question about architecture, file relationships, dependencies or component explanation:
- **When to use**: When questions of the type *"how do I..."*, *"where is..."*, *"what does..."* or *"explain architecture"* are asked.
- **Tool**: `graphify query "<question>"` or review `graphify-out/GRAPH_REPORT.md` and `graphify-out/wiki/index.md`.

---

## 16. Linters and Formatters (Ruff & Biome)
To guarantee the quality and style of code generated by Aider or the Virtual Office:
- **Python**: **Ruff** (`ruff check` and `ruff format`)
- **JavaScript / TypeScript / Web**: **Biome** (`biome check`)
- **When to use**: Always when code writing is finished before declaring a task completed.
- **Configuration**: Ensure that `ruff` and `biome` are properly configured according to the project standards before running checks.
- **Automatic Fixes**: Prefer using `ruff format` and `biome format` to automatically fix style issues before manual review.
- **Continuous Integration**: Integrate `ruff` and `biome` checks into the CI pipeline to enforce code quality consistently.

---

## 17. Common Mistakes to Avoid

- Skipping Phase 0 (complexity decision).
- Skipping Phase 1 (skill invocation) on complex tasks.
- Proceeding without user confirmation in any SDLC phase.
- Generating massive code in `OFFICE_RESULT.md`.
- Leaving test or temporary files in the root.
- Using relative Markdown links instead of absolute ones.
- Forgetting to run `Browser-Use` on UI changes.
- Ignoring the Golden Rules in section 3.9.