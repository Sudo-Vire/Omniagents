# SDLC & Execution Workflow

## 1. Phase 0 – Mandatory Decision Tree (First Step – Always Execute)
- **Simple Task** (use Simplified Flow): Correction of a single line, direct query, refactoring < 10 lines.
- **Complex Task** (use Full Workflow): Medium/large refactoring, new feature/component/endpoint, architecture/UI changes.

## 2. Standard Workflow Phases (Phases 1 to 6)
- **Phase 1**: Skill & Tool Invocation (`skill` tool, `graphify query`).
- **Phase 2**: Catalog & Agent Selection (`agency-agents` + `claude-subagents`).
- **Phase 3**: Execution with Virtual Office (`OFFICE_RESULT.md`) & Aider.
- **Phase 4**: Validation & Verification (Linting, Visual testing, Regressions).
- **Phase 5**: Git Workflow (Conventional Commits, Branching).
- **Phase 6**: Cleanup & Closure (Remove temp files, save in `session-state/files/`).

## 3. SDLC General Cycle (Phases 1 to 8)
1. Requirements & Planning
2. Design
3. Development & Implementation
4. Security & Compliance
5. Testing & Quality Assurance
6. Git Workflow & Version Control
7. Deployment & DevOps (Cloudflare)
8. Maintenance, Support & Research

*(In every phase: Think out loud → Present plan → Ask explicit confirmation → Wait for user approval).*

## 4. Golden Rules
- Never skip Phase 1 on complex tasks.
- Always use absolute Markdown links.
- Always perform visual validation of UI changes.
- Never leave test files in root.
