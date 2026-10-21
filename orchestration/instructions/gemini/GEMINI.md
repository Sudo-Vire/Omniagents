# Master Gemini Agent & Skills Instructions (GEMINI.md)

<gemini-master-instructions>
  <metadata>
    <target-model>Google Gemini (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 3.1, Gemini CLI)</target-model>
    <purpose>Exhaustive operational directives structured natively in XML for maximum instruction-following fidelity and step-by-step reasoning.</purpose>
  </metadata>

  <core-behavior-priority rule="strict">
    <step id="1">Think out loud before acting.</step>
    <step id="2">Present the plan of the current phase.</step>
    <step id="3">Ask for explicit confirmation: 'Is this correct or would you like to make any changes?'</step>
    <step id="4">Wait for explicit user approval before proceeding to the next phase or executing changes.</step>
    <step id="5">Execute only after receiving confirmation.</step>
  </core-behavior-priority>

  <section id="1" title="Local Model Gateway (Omniroute Gateway)">
    <endpoint>http://localhost:20128/v1</endpoint>
    <model>Selected local runtime model</model>
    <objective>High-speed local inference, zero external costs, absolute code privacy.</objective>
  </section>

  <section id="2" title="Operational Principles and Philosophy (Ponytail & Lazy Senior Dev)">
    <principle name="YAGNI">Minimal, surgical, direct changes. The best line of code is the one never written.</principle>
    <principle name="Action-First">Direct, to-the-point responses. Commands and code snippets first; explanations after.</principle>
    <principle name="Reusability">Prioritize standard libraries, existing code, and native features.</principle>
    <principle name="Root-Cause-Correction">Address root causes, not symptoms.</principle>
  </section>

  <section id="3" title="Standard Workflow and Execution Methodology">
    <phase id="0" name="Mandatory Decision Tree">
      <rule>Determine task complexity: Simple (YAGNI + Immediate Action) vs Complex (Full 8-phase SDLC).</rule>
    </phase>
    <phase id="1" name="Mandatory Skill and Tool Invocation">
      <rule>Invoke skill tool and Graphify query before writing code.</rule>
    </phase>
    <phase id="2" name="Catalog and Agent Selection">
      <rule>Select macro catalog (agency-agents) or tactical subagents (claude-subagents).</rule>
    </phase>
    <phase id="3" name="Execution with Virtual Office and Aider">
      <rule>Generate plan in OFFICE_RESULT.md, apply code via Aider.</rule>
    </phase>
    <phase id="4" name="Validation and Verification">
      <rule>Run linters (ruff, biome) and visual checks (Browser-Use).</rule>
    </phase>
    <phase id="5" name="Git Workflow">
      <rule>Conventional Commits and branching strategy.</rule>
    </phase>
    <phase id="6" name="Cleanup and Closure">
      <rule>Remove temporary files, store session state in session-state/files/.</rule>
    </phase>
  </section>

  <section id="4" title="Dual Collaboration Ecosystem">
    <domain area="Design">design-ui-designer.md</domain>
    <domain area="Engineering">engineering-software-architect.md, engineering-senior-developer.md</domain>
    <domain area="Security">Strix penetration testing framework</domain>
    <domain area="Product & Strategy">product-manager.md</domain>
  </section>

  <section id="5" title="Software Development Life Cycle (SDLC)">
    <lifecycle-phases>
      Phase 1: Requirements & Planning
      Phase 2: Design
      Phase 3: Development & Implementation
      Phase 4: Security & Compliance
      Phase 5: Testing & QA
      Phase 6: Git Workflow
      Phase 7: Deployment (Cloudflare)
      Phase 8: Maintenance & Research
    </lifecycle-phases>
  </section>

  <section id="6" title="Golden Rules and Common Mistakes">
    <rule>Never skip confirmation in any SDLC phase.</rule>
    <rule>Always use absolute Markdown links.</rule>
    <rule>Always perform visual validation for UI changes.</rule>
  </section>

</gemini-master-instructions>
