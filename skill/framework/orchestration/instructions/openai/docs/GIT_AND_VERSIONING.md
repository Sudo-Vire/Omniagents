# Git Standards & Versioning

> 🚨 **PRECEDENCIA SUPREMA:** Lo establecido en [PULL_REQUEST_INSTRUCTIONS.md](../PULL_REQUEST_INSTRUCTIONS.md) **primará siempre** sobre estas directivas de Git y versioning.

## 1. Branch Naming & Mandatory New Branch Rule (`git branch`)
- **Format**: `tipo/nombre` (donde `tipo` es `feature`, `bugfix` o `enhancement`).
- **Mandatory New Branch Rule**: Siempre que se inicien nuevos cambios que no tengan relación con los anteriores, o **después de finalizar/fusionar una PR**, es **estrictamente obligatorio** crear una nueva rama de trabajo. Queda prohibido reutilizar ramas anteriores o trabajar directamente en `main`/`develop`.

## 2. Commit Messages & Types
- **Types allowed**: `feature`, `bugfix`, `enhancement` (conforme a [PULL_REQUEST_INSTRUCTIONS.md](../PULL_REQUEST_INSTRUCTIONS.md)).

## 3. Versioning & Changelog (Git-Cliff)
- SemVer tags: `vMAJOR.MINOR.PATCH`
- Automated changelog command: `git-cliff -o CHANGELOG.md`

## 4. Mandatory Pull Request Instructions
Before creating any Pull Request (PR), reviewing and following [PULL_REQUEST_INSTRUCTIONS.md](../PULL_REQUEST_INSTRUCTIONS.md) is **strictly mandatory**.
