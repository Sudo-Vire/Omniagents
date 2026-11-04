# Sequential Thinking MCP

This utility integrates the official
[`@modelcontextprotocol/server-sequential-thinking`](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
stdio MCP server into compatible agent hosts.

## Requirements

- Node.js 24 or later.
- An MCP-compatible host with permission to launch local processes and download the npm package on first start.

The package is published as `@modelcontextprotocol/server-sequential-thinking`. The configuration below pins version `2.0.0`; its launcher uses `npx`, so npm downloads and caches the package the first time the host starts the server. No separate repository-wide npm install is needed.

## Host configuration

Add the matching server entry to the MCP configuration used by the target host, then restart/reload that host and confirm `sequentialthinking` is listed among its tools. The first launch may require workspace trust, server approval, or a start confirmation. Host UIs may prefix the displayed tool name with the configured server name.

### Generic stdio command

Configure the host to launch:

```text
npx -y @modelcontextprotocol/server-sequential-thinking@2.0.0
```

On Windows hosts that cannot launch `npx` directly, use `cmd` with arguments:

```json
{
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@modelcontextprotocol/server-sequential-thinking@2.0.0"
  ]
}
```

### VS Code

The skill ships a template at `adapters/vscode.mcp.json`; copy it to `.vscode/mcp.json` in your workspace. VS Code can discover this workspace configuration; trust the workspace/server if prompted, then start or reload the server from the MCP Servers view if it does not start automatically. Do not overwrite an existing `servers` object when adding the entry to another workspace.

```json
{
  "servers": {
    "sequential-thinking": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking@2.0.0"
      ]
    }
  }
}
```

### Claude Code

The skill ships `adapters/mcpServers.json`; copy it to `.mcp.json` at your project root (merge into an existing `mcpServers` object if present). When you open that project in Claude Code, the server may appear as pending approval. Review and approve `sequential-thinking` when prompted, or open `/mcp` and enable it. A checked-in project configuration does not approve itself.

To add the server to your Claude Code user configuration instead (available across projects), run:

```powershell
claude mcp add --scope user --transport stdio sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking@2.0.0
```

In PowerShell, check and verify the configured connection with:

```powershell
claude mcp list
claude mcp get sequential-thinking
```

The project-scoped repository entry is useful when you run Claude Code from this checkout. If you only install the skill globally and use Claude Code in unrelated directories, use the user-scoped command instead.

To install the **skill** itself for Claude Code, copy the complete `skill/` directory (not just `SKILL.md`) to either:

- Project scope: `<project>\.claude\skills\omniagents-orchestration\`
- User scope: `$HOME\.claude\skills\omniagents-orchestration\`

After copying, confirm that `SKILL.md`, `scripts/`, `references/`, `framework/`, and `dependencies/` are present. Start a Claude Code session in that project and invoke `/omniagents-orchestration`, or ask Claude Code to use the skill. The skill and the MCP server are separate installations: copying the skill does not register the MCP server.

### Claude Desktop

Claude Desktop and Claude Code have separate MCP configuration. In Claude Desktop, open **Settings → Developer → Edit Config** and merge the following entry into the `mcpServers` object in `claude_desktop_config.json`. On Windows, replace `command` and `args` with the `cmd` configuration shown above. Save the file, restart Claude Desktop, and verify that the server appears in its developer/MCP tools view. Installing this repository's Agent Skill does not install it into Claude Desktop.

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking@2.0.0"
      ]
    }
  }
}
```

### Codex CLI

Run:

```text
codex mcp add sequential-thinking npx -y @modelcontextprotocol/server-sequential-thinking@2.0.0
```

Other MCP hosts must register the same stdio command using their own documented configuration format. The portable framework cannot configure, approve, or reload every host automatically. The skill's `adapters/` templates are optional; no host-specific file is required to use the framework.

## Automatic check

`scripts/check_dependencies.py` (skip with `--skip-mcp-check`) and `scripts/check_mcp.py` look for a `sequential-thinking` entry in: the workspace `.vscode/mcp.json`, VS Code user `mcp.json`, project `.mcp.json`, `~/.claude.json`, Claude Desktop config, `~/.codex/config.toml`, and `~/.copilot/mcp-config.json`. If none is found they warn and, in an interactive terminal, ask whether to activate it manually, automatically, or not at all, then print a step-by-step report for that answer (`--report-file` saves it).

- Automatic activation merges the entry into the chosen host's JSON config (keeping other servers and writing a `.omniagents.bak` copy) or runs `claude mcp add` / `codex mcp add`, only after confirmation. Files with comments or unexpected structure are never rewritten; the report falls back to manual steps.
- `--probe` launches the server and verifies it lists `sequentialthinking` (uses npm/network).
- Non-interactive runs only warn. Set `OMNIAGENTS_MCP=skip` to silence the warning.
- None of this proves a running host loaded or approved the server; confirm the tool in the host's tool list.

## Framework usage

When solving a non-trivial task in the Omniagents framework, use the host's `sequentialthinking` MCP tool if it is connected and exposed:

- Architecture or design decisions with multiple viable options.
- Multi-step changes spanning framework, skills, agents, or tools.
- Difficult debugging where hypotheses need to be tested and revised.
- Risk/dependency analysis before an operation with meaningful side effects.

Do not invoke it for trivial edits or simple lookups. Use it to organize analysis; report concise conclusions, decisions, assumptions, and validation rather than exposing private internal reasoning. If the tool is not exposed, do not claim it ran: continue directly when safe and mention that the MCP was unavailable.

## Validation and privacy

After host configuration, restart/reload the host and verify that `sequentialthinking` appears in its MCP tool list. Ask for a multi-step plan and confirm the host invokes the tool. A successful repository preflight only verifies that this integration directory and its documentation exist; it does not prove that the host connected to the server.

The server communicates over local stdio. The host still controls what inputs are sent and where logs are kept. Do not send secrets or unnecessary sensitive data. Follow the upstream license and notices distributed with the npm package.

## Sources

- [Official Sequential Thinking server README](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
- [npm package](https://www.npmjs.com/package/@modelcontextprotocol/server-sequential-thinking)
