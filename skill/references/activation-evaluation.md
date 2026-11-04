# Activation evaluation cases

Use these cases to evaluate skill selection in the intended host. They are test prompts, not evidence that automatic selection was run.

## Should use the skill

1. “Coordinate independent architecture and test-plan reviews for this repository, then reconcile the findings.”
2. “Use the existing Omniagents agent catalog to split this migration into bounded, independent work and report verified outcomes.”
3. “Which repository agent and downloaded skill should handle the API contract and UI accessibility work? Delegate if the host supports it.”

## Should not use the skill

1. “Fix this one spelling mistake in the README.”
2. “Trace this function's call path across the repository.” This is one continuous trace, not independent workstreams.
3. “Run the unit tests for this file.” This is a direct tool task unless the user separately requests delegation.

## Ambiguous

1. “Review these five files for consistency.” Inspect whether this is one connected trace; work directly unless the user asks for independent reviewers or the files represent genuinely separable work.
2. “Can multiple agents help with this bug?” Explain that the repository has prompt catalogs but no callable orchestration runtime. If the host supports native delegation, ask whether the user wants independent bounded reviews; otherwise offer a direct investigation.

## Host validation status

These cases have not been evaluated in a fresh VS Code Copilot chat. Verify discovery and automatic activation separately in the intended host; Agent Skills compatibility does not guarantee selection.
