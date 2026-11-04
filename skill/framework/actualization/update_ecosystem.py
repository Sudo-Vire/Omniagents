import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

SKILL_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UTILS_DIR = os.path.join(SKILL_ROOT, "dependencies", "utils")
INSTALLATION_DIR = os.path.join(SKILL_ROOT, "dependencies", "installation")
INSTRUCTIONS_DIR = os.path.join(SKILL_ROOT, "framework", "orchestration", "instructions")
UTILS_INDEX_PATH = os.path.join(UTILS_DIR, "check_utils.txt")
SOURCES_PATH = os.path.join(UTILS_DIR, "sources.json")
UTILS_CATEGORIES = {"agents", "skills", "tools"}
GATEWAY_URL = "http://localhost:20128/v1/chat/completions"


def register_utility(category, name, index_path=UTILS_INDEX_PATH):
    if category not in UTILS_CATEGORIES:
        raise ValueError(f"Unsupported utility category: {category}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise ValueError("Resource name must use letters, numbers, dots, underscores, or hyphens.")

    entry = f"{category}/{name}"
    index = Path(index_path)
    contents = index.read_text(encoding="utf-8") if index.exists() else ""
    lines = contents.splitlines()
    if entry in (line.strip() for line in lines):
        return False

    with index.open("a", encoding="utf-8", newline="\n") as index_file:
        if contents and not contents.endswith(("\n", "\r")):
            index_file.write("\n")
        index_file.write(f"{entry}\n")
    return True


def register_source(category, name, repo, ref, license_id="", sources_path=SOURCES_PATH):
    """Pin an upstream GitHub repo so scripts/fetch_utils.py can restore the utility."""
    if category not in UTILS_CATEGORIES:
        raise ValueError(f"Unsupported utility category: {category}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise ValueError("Resource name must use letters, numbers, dots, underscores, or hyphens.")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Repository must be in owner/repo form.")
    if not re.fullmatch(r"[0-9a-f]{40}", ref):
        raise ValueError("Ref must be a full 40-character commit SHA.")

    path = Path(sources_path)
    sources = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    key = f"{category}/{name}"
    entry = {"repo": repo, "ref": ref}
    if license_id:
        entry["license"] = license_id
    if sources.get(key) == entry:
        return False
    sources[key] = entry
    path.write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8", newline="\n")
    return True


def prompt_for_source(utils_category, name):
    answer = input(
        "\nRepositorio upstream de GitHub (owner/repo) para poder restaurarlo con fetch_utils.py "
        "(Enter para omitir): "
    ).strip()
    if not answer:
        return
    ref = input("SHA de commit completo (40 caracteres) a fijar: ").strip().lower()
    license_id = input("Licencia (ej. MIT, opcional): ").strip()
    try:
        changed = register_source(utils_category, name, answer, ref, license_id)
    except ValueError as error:
        print(f"  -> No registrado en sources.json: {error}")
        return
    state = "Registrado" if changed else "Sin cambios"
    print(f"  -> {state} en: {os.path.relpath(SOURCES_PATH, SKILL_ROOT)}")


def run_installation_script(resource_path):
    print("\n--- Buscando script de instalación para el recurso ---")
    install_py = os.path.join(resource_path, "install.py")
    install_ps1 = os.path.join(resource_path, "install.ps1")
    setup_py = os.path.join(resource_path, "setup.py")

    if os.path.exists(install_py):
        command = [sys.executable, install_py]
    elif os.path.exists(setup_py):
        command = [sys.executable, setup_py, "install"]
    elif os.path.exists(install_ps1):
        command = ["powershell", "-File", install_ps1]
    else:
        print(
            "No se encontró script de instalación específico. "
            "Configura la herramienta en el host correspondiente."
        )
        return

    choice = input(
        "El script puede ejecutar acciones de instalación. "
        "¿Deseas ejecutarlo ahora? (s/N): "
    ).strip().lower()
    if choice != "s":
        print("Instalación omitida por falta de aprobación.")
        return

    result = subprocess.run(command)
    if result.returncode:
        raise subprocess.CalledProcessError(result.returncode, command)

def generate_ai_integration_block(resource_type, name):
    print(f"\n[IA Integration] Consultando al gateway de Omniroute para generar documentación detallada para '{name}'...")
    prompt = f"""
    Genera un bloque de documentación detallado en Markdown puro (sin etiquetas XML) para integrar un nuevo recurso en el ecosistema Omniagents.
    Tipo de recurso: {resource_type}
    Nombre/Identificador: {name}
    
    El bloque debe incluir:
    - Identificador y categoría.
    - Propósito y caso de uso avanzado.
    - Política de uso, integración y validación en el flujo de desarrollo.
    
    Devuelve ÚNICAMENTE el bloque en Markdown estructurado (con cabeceras h2 o h3 y listas detalladas).
    """
    
    payload = {
        "model": "openai/antigravity/gemini-3.1-flash-lite",
        "messages": [
            {"role": "system", "content": "Eres un arquitecto experto en documentación de sistemas de IA. Genera documentación técnica impecable."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    try:
        req = urllib.request.Request(
            GATEWAY_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": "Bearer local-gateway"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if content:
                print("  [OK] Bloque generado exitosamente mediante IA.")
                return content.strip()
    except Exception as e:
        print(f"  [!] Aviso: Gateway no disponible ({e}). Usando plantilla avanzada enriquecida.")
        
    return f"""## Model Context Protocol & Advanced Tooling: {name}
- **Resource Identifier**: `{name}` ({resource_type})
- **Purpose**: Advanced ecosystem extension providing specialized execution and processing capabilities.
- **Integration & Usage Policy**: Integrated natively into Omniagents tooling guidelines. Adhere to YAGNI and validation protocols when invoking.
"""

def integrate_into_instructions(resource_type, name):
    print(f"\n[Integración Inteligente con IA] Procesando '{name}' ({resource_type})...")
    
    ai_block = generate_ai_integration_block(resource_type, name)
    
    def model_docs(*parts_by_model):
        return [os.path.join(INSTRUCTIONS_DIR, *parts) for parts in parts_by_model]

    master_docs = [("claude", "CLAUDE.md"), ("others", "agents.md")]
    target_docs = []
    if "Agente" in resource_type:
        target_docs = model_docs(
            ("gemini", "docs", "AGENTS_CATALOG.md"),
            ("openai", "docs", "AGENTS_CATALOG.md"),
            ("copilot", "docs", "AGENTS_CATALOG.md"),
            *master_docs,
        )
    elif "Herramienta" in resource_type or "Framework" in resource_type or "MCP" in resource_type or "Skill" in resource_type:
        target_docs = model_docs(
            ("gemini", "docs", "TOOLING_AND_VALIDATION.md"),
            ("openai", "docs", "TOOLING_AND_VALIDATION.md"),
            ("copilot", "docs", "TOOLING_AND_VALIDATION.md"),
            *master_docs,
        )
    else:
        target_docs = model_docs(
            ("gemini", "sub-rules", "sub-rules-sdlc.md"),
            ("openai", "sub-rules", "sub-rules-sdlc.md"),
            *master_docs,
        )

    for doc_path in target_docs:
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Añadir el bloque generado por IA al final del documento de forma estructurada
            content += f"\n\n{ai_block}\n"
                
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Integrado formalmente en: {os.path.relpath(doc_path, SKILL_ROOT)}")

def main():
    print("=== Asistente Avanzado de Actualización del Ecosistema Omniagents (AI-Powered) ===")
    
    print("\n¿Qué deseas añadir al ecosistema?")
    print("1. Agente (agency-agents / claude-subagents)")
    print("2. Habilidad (Skill)")
    print("3. Herramienta / MCP Server (Tool / MCP)")
    print("4. Sub-regla / Instrucción (Sub-rule)")
    print("5. Framework / Plugin / Prompt")
    
    choice = input("\nSelecciona una opción (1-5): ").strip()
    
    types_map = {
        "1": ("Agente", os.path.join(UTILS_DIR, "agents"), "agents"),
        "2": ("Skill", os.path.join(UTILS_DIR, "skills"), "skills"),
        "3": ("Herramienta/MCP", os.path.join(UTILS_DIR, "tools"), "tools"),
        "4": (
            "Sub-regla",
            os.path.join(INSTRUCTIONS_DIR, "gemini", "sub-rules"),
            None,
        ),
        "5": ("Framework/Plugin/Prompt", os.path.join(UTILS_DIR, "tools"), "tools"),
    }
    
    if choice not in types_map:
        print("ERROR: Opción inválida. Saliendo.")
        sys.exit(1)
        
    resource_type, target_dir, utils_category = types_map[choice]
    
    name = input(f"\nIntroduce el nombre/identificador del {resource_type} (ej. 'mcp-sequential-thinking'): ").strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        print("ERROR: El identificador debe usar solo letras, números, puntos, guiones o guiones bajos.")
        sys.exit(1)
        
    resource_path = os.path.join(target_dir, name)
    exists = os.path.exists(resource_path)
    
    if exists:
        print(f"\n[AVISO] El {resource_type} '{name}' YA EXISTE en '{resource_path}'.")
        proceed = input("¿Deseas actualizarlo y re-ejecutar su instalación? (s/N): ").strip().lower()
        if proceed != 's':
            print("Operación cancelada por el usuario.")
            sys.exit(0)
    else:
        print(f"\nOK: El {resource_type} '{name}' no existe previamente. Creando directorio...")
        os.makedirs(resource_path, exist_ok=True)

    if utils_category:
        register_utility(utils_category, name, UTILS_INDEX_PATH)
        print(f"  -> Registrado en: {os.path.relpath(UTILS_INDEX_PATH, SKILL_ROOT)}")
        prompt_for_source(utils_category, name)
        
    # Integración con generación por IA
    integrate_into_instructions(resource_type, name)
    
    # La ejecución del instalador requiere aprobación explícita.
    run_installation_script(resource_path)
    
    print(
        f"\n'{name}' quedó registrado. Comprueba que sus archivos se hayan "
        "descargado o instalado y vuelve a ejecutar check_dependencies.py."
    )

if __name__ == "__main__":
    main()
