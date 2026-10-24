# Git Standard, Validation, Code Review & Common Mistakes (Modular Subfile)

## 1. Complete Git Standard (Git Workflow)
1. **Branch Naming (`git branch`)**:
   - `feature/feature-name`, `bugfix/error-description`, `hotfix/critical-description`, `refactor/module-name`, `docs/documentation-update`
2. **Commit Messages (Conventional Commits)**:
   - Format: `type(scope): brief imperative description`
   - Types: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`, `ci`, `build`
3. **Tagging and Versions (SemVer)**:
   - `vMAJOR.MINOR.PATCH`

## 2. Automated Changelog Generation (Git-Cliff)
- **Tool**: **Git-Cliff** (`git-cliff`)
- **Command**: `git-cliff -o CHANGELOG.md`

## 3. Rules of Automatic Execution and Obligatoriness
1. Mandatory skill invocation.
2. Graphify + Architecture inspection.
3. Absolute Markdown links (`[name](absolute_path)`).
4. No regressions.
5. Cleaning temporary files.

## 4. Robustness and Artifact Management
1. Defense against Nulls and DOM Failures (`if (!container) return;`).
2. Artifact Management: No test files in root. Session results exclusively in `session-state/files/`.

## 5. Code Review (Before Approving Any Change)
- Surgical precision and YAGNI
- Root cause correction
- UI/UX quality + WCAG (contrast ≥ 4.5:1, keyboard navigation, ARIA)
- No regressions
- Absolute Markdown links
- Security and privacy (no exposed credentials, no OWASP Top 10)
- Compliance with coding standards

## 6. Common Mistakes to Avoid
- Skipping Phase 0 or Phase 1.
- Proceeding without user confirmation.
- Generating massive code in `OFFICE_RESULT.md`.
- Leaving test or temporary files in root.
- Using relative Markdown links.
- Forgetting `Browser-Use` on UI changes.
- Ignoring Golden Rules.
