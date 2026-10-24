# Dual Collaboration Ecosystem – Unique Index
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

- **Nuevo Framework/Plugin/MCP/Prompt**: `mcp-sequential-thinking` (Añadido/Actualizado).

