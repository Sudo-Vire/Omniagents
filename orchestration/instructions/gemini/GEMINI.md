# Google Gemini Master XML-Native Instructions (GEMINI.md)

<omniagent-gemini-instructions>
  <metadata>
    <target-model>Google Gemini (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 3.1, Gemini CLI)</target-model>
    <purpose>Permanent, exhaustive operational directives structured natively in XML for maximum instruction-following fidelity, step-by-step reasoning, and full rulebook retention.</purpose>
  </metadata>

  <core-behavior-priority rule="strict">
    <step id="1">Think out loud before acting.</step>
    <step id="2">Present the plan of the current phase.</step>
    <step id="3">Ask for explicit confirmation: 'Is this correct or would you like to make any changes?'</step>
    <step id="4">Wait for explicit user approval before proceeding to the next phase or executing changes.</step>
    <step id="5">Execute only after receiving confirmation.</step>
  </core-behavior-priority>

  <section id="1" title="Local Model Gateway (Omniroute Gateway)">
    <description>Both the Virtual Office and Aider operate natively connected to the local Omniroute gateway:</description>
    <endpoint>http://localhost:20128/v1</endpoint>
    <model>Use the selected one</model>
    <purpose>Ensure high-speed local inference, zero external costs, and absolute privacy of the source code.</purpose>
  </section>

  <section id="2" title="Operational Principles and Philosophy (Ponytail & Lazy Senior Dev)">
    <principle name="YAGNI">The best line of code is the one that never gets written. Minimal, surgical, and direct changes.</principle>
    <principle name="Action-First">Direct, to-the-point responses. Commands, paths, or code snippets first; explanations later.</principle>
    <principle name="Reusability">Prioritize standard libraries, existing code, and native features before adding new dependencies or abstractions.</principle>
    <principle name="Root-Cause-Correction">Address the root cause of problems, not the symptoms.</principle>
  </section>

  <section id="3" title="Standard Workflow and Execution Methodology (Mandatory for All Tasks)">
    <description>This section defines exactly the step-by-step process the assistant must follow in all interactions, prompts, refactorizations, reviews, or code development.</description>
    
    <subsection id="3.1" title="Phase 0 – Mandatory Decision Tree (First Step – Always Execute)">
      <rule>Before doing anything else, decide task complexity:</rule>
      <task-type name="Simple Task">Correction of a single line/error, direct query, refactoring < 10 lines, small comment.</task-type>
      <task-type name="Complex Task">Medium/large refactoring, new feature/component/endpoint, architecture, UI/UX, security, testing, multi-file changes.</task-type>
      <rule>If in doubt, treat the task as Complex.</rule>
    </subsection>

    <subsection id="3.2" title="Phase 1 – Mandatory Skill and Tool Invocation">
      <step>Invoke the skill tool corresponding to task domain.</step>
      <step>Execute `graphify query "<question>"` and review ARCHITECTURE.md if task touches structure/architecture.</step>
      <step>Invoke Strix or security agent if task has security risks.</step>
    </subsection>

    <subsection id="3.3" title="Phase 2 – Catalog and Agent Selection">
      <choice type="Macro">agency-agents for general engineering, architecture, backend, frontend, UI/UX, security, product.</choice>
      <choice type="Tactical">claude-subagents for granular language/framework specialization.</choice>
    </subsection>

    <subsection id="3.4" title="Phase 3 – Execution with Virtual Office and Aider">
      <tool name="Virtual Office">Generates detailed plan/report in OFFICE_RESULT.md without massive code.</tool>
      <tool name="Aider">Takes OFFICE_RESULT.md context and writes, refactors, and commits actual code.</tool>
    </subsection>

    <subsection id="3.5" title="Phase 4 – Validation and Verification">
      <check type="Linting">Python -> ruff check + ruff format. JS/TS -> biome check.</check>
      <check type="Visual">Browser-Use or native tools for UI validation.</check>
      <check type="Regression">Verify existing behavior is intact.</check>
      <check type="Security">OWASP Top 10 check, Strix scan.</check>
    </subsection>

    <subsection id="3.6" title="Phase 5 – Git Workflow">
      <rule>Apply Complete Git Standard: branch naming, Conventional Commits, git-cliff changelogs.</rule>
    </subsection>

    <subsection id="3.7" title="Phase 6 – Cleanup and Closure">
      <rule>Remove temporary files, save session results in session-state/files/, absolute Markdown links, documentation check.</rule>
    </subsection>

    <subsection id="3.8" title="Simplified Flow (YAGNI + Immediate Action)">
      <rule>Analyze with YAGNI -> Minimal surgical change -> Linters -> Visual validation -> Conventional commit -> Close.</rule>
    </subsection>

    <subsection id="3.9" title="Golden Rules (Never skip)">
      <rule>Never skip Phase 1 when task is complex.</rule>
      <rule>Always use absolute Markdown links.</rule>
      <rule>Always perform visual validation of UI changes.</rule>
      <rule>Never leave test files in root.</rule>
    </subsection>
  </section>

  <section id="4" title="Dual Collaboration Ecosystem – Unique Index">
    <ecosystem-domain name="Design">UI/UX, accessibility, design systems (design-ui-designer.md)</ecosystem-domain>
    <ecosystem-domain name="Engineering">Architecture, backend, frontend, databases (engineering-software-architect.md)</ecosystem-domain>
    <ecosystem-domain name="Cybersecurity">OWASP Top 10, penetration testing (Strix)</ecosystem-domain>
    <ecosystem-domain name="Product & Strategy">Requirements, user stories, MVP (product-manager.md)</ecosystem-domain>
    <ecosystem-domain name="Marketing & Content">Copywriting, SEO, tone of voice</ecosystem-domain>
    <ecosystem-domain name="Finance & FinOps">Financial modeling, cost optimization</ecosystem-domain>
    <ecosystem-domain name="Testing & QA">Unit, integration, E2E, Browser-Use validation</ecosystem-domain>
  </section>

  <section id="5" title="SDLC – Software Development Life Cycle">
    <sdlc-phase number="1">Requirements & Planning (Superpowers + Karpathy skills)</sdlc-phase>
    <sdlc-phase number="2">Design</sdlc-phase>
    <sdlc-phase number="3">Development & Implementation</sdlc-phase>
    <sdlc-phase number="4">Security & Compliance</sdlc-phase>
    <sdlc-phase number="5">Testing & QA</sdlc-phase>
    <sdlc-phase number="6">Git Workflow & Version Control</sdlc-phase>
    <sdlc-phase number="7">Deployment & DevOps (Cloudflare)</sdlc-phase>
    <sdlc-phase number="8">Maintenance, Support & Research</sdlc-phase>
  </section>

  <section id="6" title="Git Standard & Version Control">
    <rule>Branch naming conventions (feature/, bugfix/, hotfix/, refactor/, docs/).</rule>
    <rule>Conventional Commits format: type(scope): description.</rule>
    <rule>Semantic Versioning (vMAJOR.MINOR.PATCH).</rule>
  </section>

  <section id="7" title="Changelog Generation (Git-Cliff)">
    <command>git-cliff -o CHANGELOG.md</command>
  </section>

  <section id="8" title="Superpowers Framework">
    <skills>brainstorming, test-driven-development, systematic-debugging, writing-plans, executing-plans</skills>
  </section>

  <section id="9" title="Andrej Karpathy Skills">
    <rules>Think before coding, Simplicity first, Surgical changes, Goal-driven execution.</rules>
  </section>

  <section id="10" title="Browser-Use E2E Testing">
    <rule>Mandatory visual regression and flow verification using Browser-Use before task completion.</rule>
  </section>

  <section id="11" title="Automation & Automatic Execution Rules">
    <rule>Mandatory skill invocation, Graphify architecture inspection, absolute Markdown links, no regressions, cleaning.</rule>
  </section>

  <section id="12" title="Linters and Formatters">
    <tool name="Python">Ruff (`ruff check`, `ruff format`)</tool>
    <tool name="Web">Biome (`biome check`)</tool>
  </section>

</omniagent-gemini-instructions>
