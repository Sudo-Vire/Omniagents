# Git Standards & Versioning

## 1. Branch Naming (`git branch`)
- `feature/feature-name`
- `bugfix/error-description`
- `hotfix/critical-description`
- `refactor/module-name`
- `docs/documentation-update`

## 2. Commit Messages (Conventional Commits)
- **Format**: `type(scope): brief imperative description`
- **Types**: `feat`, `fix`, `refactor`, `perf`, `style`, `docs`, `test`, `chore`, `ci`, `build`

## 3. Versioning & Changelog (Git-Cliff)
- SemVer tags: `vMAJOR.MINOR.PATCH`
- Automated changelog command: `git-cliff -o CHANGELOG.md`
