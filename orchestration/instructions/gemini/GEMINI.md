# Google Gemini Master Agent Instructions (GEMINI.md)

<gemini-master-instructions>
  <metadata>
    <target-model>Google Gemini (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 3.1, Gemini CLI)</target-model>
    <purpose>Permanent, exhaustive operational directives structured natively in XML for maximum instruction-following fidelity, autonomous agent execution, and full rulebook retention.</purpose>
  </metadata>

  <verification-commands>
    <command type="install">python -m pip install -r installation/requirements.txt</command>
    <command type="test">pytest</command>
    <command type="compile">python -m py_compile tools/*.py installation/*.py</command>
    <command type="lint">ruff check . && biome check .</command>
  </verification-commands>

  <security-and-constraints>
    <constraint>Never expose credentials or API keys; use environment variables or .env.</constraint>
    <constraint>Respect strict module boundaries: installation/ (official downloads), pre-downloaded/ (local assets), orchestration/ (agent instructions).</constraint>
  </security-and-constraints>

  <gemini-features>
    <feature name="File Modularization">Use @file syntax (e.g., @./orchestration/instructions/gemini/gemini-config.json) to import context modularly.</feature>
    <feature name="Hierarchical Inheritance">Gemini automatically merges global instructions (~/.gemini/GEMINI.md) with repository root GEMINI.md and subdirectory GEMINI.md files.</feature>
  </gemini-features>

  <core-behavior-priority rule="strict">
    <step id="1">Think out loud before acting.</step>
    <step id="2">Present the plan of the current phase.</step>
    <step id="3">Ask for explicit confirmation: 'Is this correct or would you like to make any changes?'</step>
    <step id="4">Wait for explicit user approval before proceeding to the next phase or executing changes.</step>
    <step id="5">Execute only after receiving confirmation.</step>
  </core-behavior-priority>

  <section id="1" title="Local Model Gateway (Omniroute Gateway)">
    <endpoint>http://localhost:20128/v1</endpoint>
    <model>openai/antigravity/gemini-3.1-flash-lite</model>
    <purpose>Ensure high-speed local inference, zero external costs, and absolute privacy of the source code.</purpose>
  </section>

  <section id="2" title="Operational Principles and Philosophy (Ponytail & Lazy Senior Dev)">
    <principle name="YAGNI">The best line of code is the one that never gets written. Minimal, surgical, and direct changes.</principle>
    <principle name="Action-First">Direct, to-the-point responses. Commands, paths, or code snippets first; explanations later.</principle>
    <principle name="Reusability">Prioritize standard libraries, existing code, and native features.</principle>
    <principle name="Root-Cause-Correction">Address the root cause of problems, not the symptoms.</principle>
  </section>

  <section id="3" title="Standard Workflow and Execution Methodology (Mandatory for All Tasks)">
    <subsection id="3.1" title="Phase 0 – Mandatory Decision Tree">
      <rule>Determine task complexity: Simple Task (YAGNI + Immediate Action) vs Complex Task (Full 8-phase SDLC).</rule>
    </subsection>
    <subsection id="3.2" title="Phase 1 – Mandatory Skill and Tool Invocation">
      <rule>Invoke skill tool and Graphify query before writing code.</rule>
    </subsection>
    <subsection id="3.3" title="Phase 2 – Catalog and Agent Selection">
      <rule>Select macro catalog (agency-agents) or tactical subagents (claude-subagents).</rule>
    </subsection>
    <subsection id="3.4" title="Phase 3 – Execution with Virtual Office and Aider">
      <rule>Generate plan in OFFICE_RESULT.md, apply code via Aider.</rule>
    </subsection>
    <subsection id="3.5" title="Phase 4 – Validation and Verification">
      <rule>Run linters (ruff, biome) and visual checks (Browser-Use).</rule>
    </subsection>
    <subsection id="3.6" title="Phase 5 – Git Workflow">
      <rule>Apply Complete Git Standard: branch naming, Conventional Commits, git-cliff changelogs.</rule>
    </subsection>
    <subsection id="3.7" title="Phase 6 – Cleanup and Closure">
      <rule>Remove temporary files, store session results in session-state/files/, absolute Markdown links.</rule>
    </subsection>
  </section>

  <section id="4" title="Dual Collaboration Ecosystem">
    <domain area="Design">UI/UX, accessibility, design systems (design-ui-designer.md)</domain>
    <domain area="Engineering">Architecture, backend, frontend, databases (engineering-software-architect.md)</domain>
    <domain area="Cybersecurity">OWASP Top 10, penetration testing (Strix)</domain>
    <domain area="Product & Strategy">Requirements, user stories, MVP (product-manager.md)</domain>
  </section>

  <section id="5" title="SDLC – Software Development Life Cycle">
    <sdlc-phase number="1">Requirements & Planning</sdlc-phase>
    <sdlc-phase number="2">Design</sdlc-phase>
    <sdlc-phase number="3">Development & Implementation</sdlc-phase>
    <sdlc-phase number="4">Security & Compliance</sdlc-phase>
    <sdlc-phase number="5">Testing & QA</sdlc-phase>
    <sdlc-phase number="6">Git Workflow & Version Control</sdlc-phase>
    <sdlc-phase number="7">Deployment & DevOps (Cloudflare)</sdlc-phase>
    <sdlc-phase number="8">Maintenance, Support & Research</sdlc-phase>
  </section>

  <section id="6" title="Golden Rules and Common Mistakes">
    <rule>Never skip confirmation in any SDLC phase.</rule>
    <rule>Always use absolute Markdown links.</rule>
    <rule>Always perform visual validation of UI changes.</rule>
    <rule>Never leave test files in root.</rule>
  </section>

</gemini-master-instructions>
