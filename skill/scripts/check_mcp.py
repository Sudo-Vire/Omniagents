#!/usr/bin/env python3
"""Detect whether the Sequential Thinking MCP is configured and help enable it.

The script can only inspect host configuration files and test that the server
launches. It cannot know whether a running host loaded or approved the server;
that must be confirmed in the host's tool list.
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable

SERVER_NAME = "sequential-thinking"
PACKAGE = "@modelcontextprotocol/server-sequential-thinking@2.0.0"
TOOL_NAME = "sequentialthinking"
MIN_NODE_MAJOR = 24
SKIP_ENV = "OMNIAGENTS_MCP"
SKILL_PARENT_PARTS = ((".claude", "skills"), (".agents", "skills"), (".github", "skills"))

HOSTS = {
    "vscode": {"label": "VS Code (workspace)", "kind": "json", "root": "servers", "typed": True},
    "claude-code": {"label": "Claude Code (proyecto)", "kind": "json", "root": "mcpServers", "typed": True},
    "claude-code-user": {"label": "Claude Code (usuario, CLI)", "kind": "cli"},
    "claude-desktop": {"label": "Claude Desktop", "kind": "json", "root": "mcpServers", "typed": False},
    "codex": {"label": "Codex CLI", "kind": "cli"},
    "other": {"label": "Otro host MCP", "kind": "manual"},
}
AUTO_HOSTS = tuple(key for key, host in HOSTS.items() if host["kind"] != "manual")


def _config_dir(app: str) -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / app


def host_config_path(host: str, project_dir: Path) -> Path | None:
    if host == "vscode":
        return project_dir / ".vscode" / "mcp.json"
    if host == "claude-code":
        return project_dir / ".mcp.json"
    if host == "claude-desktop":
        return _config_dir("Claude") / "claude_desktop_config.json"
    return None


def config_candidates(project_dir: Path) -> list[tuple[str, Path]]:
    home = Path.home()
    return [
        ("VS Code (workspace)", project_dir / ".vscode" / "mcp.json"),
        ("VS Code (usuario)", _config_dir("Code") / "User" / "mcp.json"),
        ("Claude Code (proyecto)", project_dir / ".mcp.json"),
        ("Claude Code (usuario)", home / ".claude.json"),
        ("Claude Desktop", _config_dir("Claude") / "claude_desktop_config.json"),
        ("Codex CLI", home / ".codex" / "config.toml"),
        ("GitHub Copilot CLI", home / ".copilot" / "mcp-config.json"),
    ]


def find_configured(project_dir: Path) -> list[tuple[str, Path]]:
    found = []
    for label, path in config_candidates(project_dir):
        try:
            if SERVER_NAME in path.read_text(encoding="utf-8", errors="ignore"):
                found.append((label, path))
        except OSError:
            continue
    return found


def guess_project_dir(skill_root: Path, cwd: Path) -> Path:
    """Use the cwd, unless it is inside the skill installed under <project>/.<host>/skills."""
    skill_root, cwd = skill_root.resolve(), cwd.resolve()
    if skill_root != cwd and skill_root not in cwd.parents:
        return cwd
    for parent in skill_root.parents:
        relative = skill_root.relative_to(parent).parts
        if any(relative[:2] == parts for parts in SKILL_PARENT_PARTS):
            return parent
    return cwd


def check_node() -> tuple[bool, str]:
    node = shutil.which("node")
    if not node:
        return False, f"Node.js no encontrado (se requiere {MIN_NODE_MAJOR}+)"
    try:
        version = subprocess.run(
            [node, "--version"], capture_output=True, text=True, timeout=15
        ).stdout.strip()
        major = int(version.lstrip("v").split(".")[0])
    except (OSError, ValueError, subprocess.SubprocessError):
        return False, "No se pudo leer la versión de Node.js"
    if major < MIN_NODE_MAJOR:
        return False, f"Node.js {version} es demasiado antiguo (se requiere {MIN_NODE_MAJOR}+)"
    return True, f"Node.js {version}"


def probe_server(timeout: float = 120.0) -> tuple[bool, str]:
    """Launch the server and confirm it lists the sequentialthinking tool."""
    npx = shutil.which("npx")
    if not npx:
        return False, "npx no encontrado"
    try:
        proc = subprocess.Popen(
            [npx, "-y", PACKAGE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
        )
    except OSError as error:
        return False, f"No se pudo lanzar npx: {error}"

    lines: queue.Queue = queue.Queue()

    def read_output() -> None:
        for line in proc.stdout:
            lines.put(line)
        lines.put(None)

    threading.Thread(target=read_output, daemon=True).start()
    deadline = time.monotonic() + timeout

    def send(message: dict) -> None:
        proc.stdin.write(json.dumps(message) + "\n")
        proc.stdin.flush()

    def wait_for(message_id: int) -> dict | None:
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=0.5)
            except queue.Empty:
                continue
            if line is None:
                return None
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if message.get("id") == message_id:
                return message
        return None

    try:
        send({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "omniagents-check", "version": "1.0"},
            },
        })
        if wait_for(1) is None:
            return False, "El servidor no respondió a initialize (¿sin red o npm bloqueado?)"
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        response = wait_for(2)
        if response is None:
            return False, "El servidor no respondió a tools/list"
        names = [tool.get("name") for tool in response.get("result", {}).get("tools", [])]
        if TOOL_NAME not in names:
            return False, f"El servidor arrancó pero no expone '{TOOL_NAME}' (expone: {names})"
        return True, f"El servidor arranca y expone '{TOOL_NAME}'"
    except OSError as error:
        return False, f"Error de comunicación con el servidor: {error}"
    finally:
        try:
            proc.stdin.close()
            proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            proc.kill()


def server_entry(host: str) -> dict:
    entry = {"command": "npx", "args": ["-y", PACKAGE]}
    if HOSTS[host].get("typed"):
        entry = {"type": "stdio", **entry}
    if host == "claude-desktop" and sys.platform == "win32":
        entry = {"command": "cmd", "args": ["/c", "npx", "-y", PACKAGE]}
    return entry


def cli_command(host: str) -> list[str]:
    if host == "claude-code-user":
        launcher = ["cmd", "/c", "npx"] if sys.platform == "win32" else ["npx"]
        return ["claude", "mcp", "add", "--scope", "user", "--transport", "stdio",
                SERVER_NAME, "--", *launcher, "-y", PACKAGE]
    if host == "codex":
        return ["codex", "mcp", "add", SERVER_NAME, "npx", "-y", PACKAGE]
    raise ValueError(f"{host} no tiene comando CLI")


def merge_server_config(path: Path, root_key: str, entry: dict) -> bool:
    """Add the server to a JSON config without touching other servers.

    Returns False when it is already present. Raises ValueError for files it
    cannot safely rewrite (invalid JSON, comments, unexpected structure).
    """
    data: dict = {}
    existed = path.is_file()
    if existed:
        text = path.read_text(encoding="utf-8")
        if text.strip():
            try:
                data = json.loads(text)
            except ValueError as error:
                raise ValueError(f"{path} no es JSON estricto (¿comentarios?): {error}") from error
        if not isinstance(data, dict):
            raise ValueError(f"{path} no contiene un objeto JSON")
    servers = data.setdefault(root_key, {})
    if not isinstance(servers, dict):
        raise ValueError(f"'{root_key}' en {path} no es un objeto")
    if SERVER_NAME in servers:
        return False
    servers[SERVER_NAME] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    if existed:
        shutil.copy2(path, path.with_name(path.name + ".omniagents.bak"))
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return True


def host_steps(host: str, project_dir: Path) -> list[str]:
    command = f"npx -y {PACKAGE}"
    if host == "vscode":
        path = host_config_path(host, project_dir)
        return [
            f"Copia `<skill-root>/dependencies/utils/tools/mcp-sequential-thinking/adapters/vscode.mcp.json` a `{path}`. Si ya existe, añade solo la entrada `{SERVER_NAME}` dentro de `servers`.",
            "Abre el workspace en VS Code y confía en él si lo pide.",
            "Abre la vista de servidores MCP (comando `MCP: List Servers`), arranca `sequential-thinking` y acepta la confirmación de confianza.",
        ]
    if host == "claude-code":
        path = host_config_path(host, project_dir)
        return [
            f"Copia `<skill-root>/dependencies/utils/tools/mcp-sequential-thinking/adapters/mcpServers.json` a `{path}`. Si ya existe, fusiona la entrada en `mcpServers`.",
            "Abre Claude Code en ese proyecto.",
            "Aprueba `sequential-thinking` cuando aparezca como pendiente, o actívalo desde `/mcp`. El archivo no se aprueba solo.",
        ]
    if host == "claude-code-user":
        return [
            f"Ejecuta: `{' '.join(cli_command(host))}`.",
            "Abre una sesión nueva de Claude Code; ejecuta `claude mcp list` y confirma que `sequential-thinking` aparece.",
        ]
    if host == "claude-desktop":
        return [
            f"En Claude Desktop abre Ajustes → Developer → Edit Config y fusiona en `mcpServers` la entrada `{SERVER_NAME}` (plantilla `adapters/mcpServers.json`; en Windows usa `cmd` con `/c npx ...` si `npx` no arranca).",
            "Guarda y reinicia Claude Desktop por completo.",
        ]
    if host == "codex":
        return [f"Ejecuta: `{' '.join(cli_command(host))}`.", "Reinicia Codex CLI."]
    return [
        f"Registra en tu host un servidor MCP stdio con el comando `{command}` (consulta la documentación de configuración MCP de tu host).",
        "Si el host no puede lanzar `npx` directamente en Windows, usa `cmd /c npx -y ...`.",
        "Aprueba o confía en el servidor si el host lo solicita y reinicia el host.",
    ]


def host_cli_status(timeout: float = 120.0) -> list[tuple[str, str, str]]:
    """Ask host CLIs that can health-check MCP servers (`<cli> mcp list`).

    Returns (cli, state, detail) with state in connected, not-connected, not-listed,
    or error. Hosts without such a CLI (VS Code, Claude Desktop) cannot be checked here.
    """
    results = []
    for cli in ("claude", "codex"):
        executable = shutil.which(cli)
        if not executable:
            continue
        try:
            completed = subprocess.run(
                [executable, "mcp", "list"], capture_output=True, text=True, timeout=timeout,
                encoding="utf-8", errors="replace",
            )
        except (OSError, subprocess.SubprocessError) as error:
            results.append((cli, "error", str(error)))
            continue
        output = (completed.stdout or "") + (completed.stderr or "")
        line = next((l.strip() for l in output.splitlines() if SERVER_NAME in l), "")
        lowered = line.lower()
        if not line:
            state = "error" if completed.returncode != 0 else "not-listed"
            line = output.strip()[:200] or "sin salida"
        elif "connected" in lowered and "not connected" not in lowered and "failed" not in lowered:
            state = "connected"
        else:
            state = "not-connected"
        results.append((cli, state, line))
    return results


def host_check(out: Callable[[str], None] = print) -> int:
    results = host_cli_status()
    if not results:
        out("No hay ninguna CLI de host (claude, codex) en el PATH, así que no se puede comprobar desde aquí.")
        out("En VS Code: `MCP: List Servers` debe mostrar `sequential-thinking` en ejecución, y el selector de herramientas del chat debe listar `" + TOOL_NAME + "`.")
        return 2
    connected = False
    for cli, state, detail in results:
        out(f"{cli}: {state} - {detail}")
        connected = connected or state == "connected"
    if any(state != "error" for _, state, _ in results):
        out("Esto confirma que la CLI conecta con el servidor, no que una sesión ya abierta lo tenga cargada: reinicia la sesión y comprueba que aparece `" + TOOL_NAME + "`.")
    else:
        out("La CLI no se pudo ejecutar; comprueba el host manualmente (lista de herramientas del host).")
    return 0 if connected else 1


def build_report(
    choice: str,
    host: str,
    project_dir: Path,
    node: tuple[bool, str],
    npx_found: bool,
    configured: list[tuple[str, Path]],
    actions: list[str],
    probe: tuple[bool, str] | None,
) -> str:
    lines = ["# Informe de activación: Sequential Thinking MCP", "", "## Estado detectado", ""]
    lines.append(f"- Node.js: {'OK' if node[0] else 'PROBLEMA'} — {node[1]}")
    lines.append(f"- npx: {'encontrado' if npx_found else 'NO encontrado'}")
    if configured:
        lines.append("- Configuración encontrada en: " + "; ".join(f"{label} (`{path}`)" for label, path in configured))
    else:
        lines.append("- Configuración encontrada: ninguna")
    lines.append(f"- Proyecto asumido: `{project_dir}`")
    lines.append("- Límite: el script solo lee archivos de configuración; no puede saber si el host cargó el servidor. Confírmalo en la lista de herramientas del host.")
    labels = {"manual": "activar manualmente", "auto": "activar automáticamente", "skip": "no activar"}
    lines += ["", f"## Decisión del usuario: {labels[choice]}", ""]

    if choice == "skip":
        lines += [
            "No se ha cambiado ningún archivo. El framework continúa sin `sequentialthinking`, sin simular que se usó.",
            f"Para activarlo más tarde ejecuta `python <skill-root>/scripts/check_mcp.py`. Para silenciar este aviso, define la variable de entorno `{SKIP_ENV}=skip`.",
        ]
        return "\n".join(lines) + "\n"

    lines += [f"## Pasos para {HOSTS[host]['label']}", ""]
    number = 1
    if not node[0]:
        lines.append(f"{number}. Instala Node.js {MIN_NODE_MAJOR} o superior (https://nodejs.org) y abre una terminal nueva.")
        number += 1
    if actions:
        for action in actions:
            lines.append(f"{number}. [Hecho por el script] {action}")
            number += 1
        steps = host_steps(host, project_dir)[1:]
    else:
        steps = host_steps(host, project_dir)
    for step in steps:
        lines.append(f"{number}. {step}")
        number += 1
    lines += [
        f"{number}. Recarga o reinicia el host y confirma que `{TOOL_NAME}` aparece en su lista de herramientas (el host puede mostrarla con el prefijo `{SERVER_NAME}`).",
        f"{number + 1}. Pide un plan de varios pasos y comprueba que el host invoca la herramienta.",
        f"{number + 2}. Con Claude Code o Codex puedes comprobar la conexión con `python <skill-root>/scripts/check_mcp.py --host-check` (ejecuta `<cli> mcp list`).",
        "",
        "## Verificación del servidor",
        "",
    ]
    if probe is None:
        lines.append(f"No se ejecutó la prueba. Puedes lanzarla con `python <skill-root>/scripts/check_mcp.py --probe` (descarga `{PACKAGE}` con npm la primera vez).")
    else:
        lines.append(f"- Prueba de arranque: {'OK' if probe[0] else 'FALLÓ'} — {probe[1]}")
    lines += [
        "",
        "## Si algo falla",
        "",
        "- `npx` no se encuentra o falla: revisa Node.js y el acceso a npm; en Windows prueba `cmd /c npx ...`.",
        "- El host no lista la herramienta: está sin aprobar o sin recargar; busca el servidor pendiente en la interfaz MCP del host.",
        "- Configuración existente con comentarios: el script no la reescribe; añade la entrada a mano.",
        "- Detalles por host: `<skill-root>/dependencies/utils/tools/mcp-sequential-thinking/README.md`.",
    ]
    return "\n".join(lines) + "\n"


def _choose(ask: Callable[[str], str], out: Callable[[str], None], prompt: str, options: dict[str, str]) -> str:
    while True:
        out(prompt)
        for key, label in options.items():
            out(f"  {key}) {label}")
        answer = ask("Opción: ").strip().lower()
        if answer in options:
            return answer
        out("Opción no válida.")


def run(
    skill_root: Path,
    project_dir: Path,
    choice: str | None = None,
    host: str | None = None,
    report_file: Path | None = None,
    probe: bool = False,
    interactive: bool = False,
    ask: Callable[[str], str] = input,
    out: Callable[[str], None] = print,
) -> int:
    node = check_node()
    npx_found = shutil.which("npx") is not None
    configured = find_configured(project_dir)

    if configured:
        out("MCP Sequential Thinking: configuración encontrada en " + "; ".join(f"{l} ({p})" for l, p in configured))
        out("  El script no puede confirmar que el host lo haya cargado: comprueba que aparece la herramienta " + TOOL_NAME + ".")
        if probe:
            ok, detail = probe_server()
            out(f"  Prueba de arranque: {'OK' if ok else 'FALLÓ'} - {detail}")
            return 0 if ok else 1
        return 0

    if os.environ.get(SKIP_ENV, "").lower() == "skip" and choice is None:
        out(f"MCP Sequential Thinking no configurado; aviso omitido por {SKIP_ENV}=skip.")
        return 0

    out("AVISO: el MCP Sequential Thinking no está configurado en ningún host detectado.")
    if not node[0]:
        out(f"  {node[1]}.")
    if choice is None:
        if not interactive:
            out("  Ejecuta `python <skill-root>/scripts/check_mcp.py` para activarlo (manual, automático) o descartarlo.")
            return 0
        answer = _choose(ask, out, "¿Cómo quieres proceder?", {
            "1": "Activarlo manualmente (genero un informe paso a paso)",
            "2": "Activarlo automáticamente (modifico la configuración del host que elijas, con tu confirmación)",
            "3": "No activarlo (el framework seguirá sin él)",
        })
        choice = {"1": "manual", "2": "auto", "3": "skip"}[answer]

    actions: list[str] = []
    probe_result: tuple[bool, str] | None = None
    exit_code = 0

    if choice != "skip" and host is None:
        if not interactive:
            host = "other"
        else:
            options = {str(i): HOSTS[key]["label"] for i, key in enumerate(AUTO_HOSTS if choice == "auto" else HOSTS, 1)}
            keys = list(AUTO_HOSTS if choice == "auto" else HOSTS)
            host = keys[int(_choose(ask, out, "¿Para qué host?", options)) - 1]
    host = host or "other"

    if choice == "auto":
        if HOSTS[host]["kind"] == "manual":
            out("La activación automática no está disponible para ese host; se genera el informe manual.")
            choice = "manual"
        else:
            if HOSTS[host]["kind"] == "json":
                target = host_config_path(host, project_dir)
                description = f"añadir la entrada `{SERVER_NAME}` a {target}"
            else:
                target = None
                description = "ejecutar: " + " ".join(cli_command(host))
            out(f"Voy a {description}")
            if interactive and ask("¿Confirmas? (s/N): ").strip().lower() != "s":
                out("Cancelado; no se ha modificado nada.")
                choice = "manual"
            else:
                try:
                    if target is not None:
                        if host == "claude-desktop" and not target.parent.is_dir():
                            raise ValueError(f"No existe {target.parent}; Claude Desktop no parece instalado")
                        added = merge_server_config(target, HOSTS[host]["root"], server_entry(host))
                        actions.append(f"Entrada añadida en `{target}`." if added else f"`{target}` ya contenía `{SERVER_NAME}`; sin cambios.")
                    else:
                        executable = shutil.which(cli_command(host)[0])
                        if not executable:
                            raise ValueError(f"`{cli_command(host)[0]}` no está en el PATH")
                        result = subprocess.run([executable, *cli_command(host)[1:]], capture_output=True, text=True, timeout=120)
                        if result.returncode != 0:
                            raise ValueError((result.stderr or result.stdout).strip() or "el comando falló")
                        actions.append(f"Ejecutado `{' '.join(cli_command(host))}`.")
                    out("  Hecho. El host aún debe recargarse y aprobar el servidor.")
                except (ValueError, OSError, subprocess.SubprocessError) as error:
                    out(f"  No se pudo activar automáticamente: {error}. Se genera el informe manual.")
                    choice = "manual"
                    exit_code = 1
        if (
            choice == "auto"
            and not probe
            and interactive
            and ask(f"¿Verificar ahora que el servidor arranca? Descarga {PACKAGE} con npm (s/N): ").strip().lower() == "s"
        ):
            probe = True

    if probe and choice != "skip":
        probe_result = probe_server()

    report = build_report(choice, host, project_dir, node, npx_found, configured, actions, probe_result)
    out("")
    out(report)
    if report_file is not None:
        report_file.write_text(report, encoding="utf-8", newline="\n")
        out(f"Informe guardado en {report_file}")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Comprueba y ayuda a activar el MCP Sequential Thinking.")
    parser.add_argument("--project-dir", type=Path, help="Proyecto del host (por defecto, el directorio actual).")
    parser.add_argument("--choice", choices=("manual", "auto", "skip"), help="Respuesta sin preguntar.")
    parser.add_argument("--host", choices=tuple(HOSTS), help="Host objetivo para manual/auto.")
    parser.add_argument("--report-file", type=Path, help="Guarda el informe en este archivo.")
    parser.add_argument("--probe", action="store_true", help="Lanza el servidor y comprueba que expone la herramienta (usa npm/red).")
    parser.add_argument("--host-check", action="store_true", help="Pregunta a las CLI de host (claude, codex) si el servidor está conectado.")
    args = parser.parse_args(argv)

    if args.host_check:
        return host_check()

    skill_root = Path(__file__).resolve().parents[1]
    project_dir = (args.project_dir or guess_project_dir(skill_root, Path.cwd())).resolve()
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    return run(
        skill_root, project_dir, args.choice, args.host, args.report_file,
        args.probe, interactive,
    )


if __name__ == "__main__":
    raise SystemExit(main())
