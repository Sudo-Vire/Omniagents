import os
import sys
import subprocess
import json
import urllib.request

ECOSYSTEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRE_DOWNLOADED_DIR = os.path.join(ECOSYSTEM_ROOT, "pre-downloaded")
INSTALLATION_DIR = os.path.join(ECOSYSTEM_ROOT, "installation")
INSTRUCTIONS_DIR = os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions")
GATEWAY_URL = "http://localhost:20128/v1/chat/completions"

def run_installation_script(resource_path):
    print("\n--- Buscando script de instalación para el recurso ---")
    install_py = os.path.join(resource_path, "install.py")
    install_ps1 = os.path.join(resource_path, "install.ps1")
    setup_py = os.path.join(resource_path, "setup.py")
    
    if os.path.exists(install_py):
        print(f"Ejecutando script Python de instalación: {install_py}")
        subprocess.run([sys.executable, install_py])
    elif os.path.exists(setup_py):
        print(f"Ejecutando setup.py: {setup_py}")
        subprocess.run([sys.executable, setup_py, "install"])
    elif os.path.exists(install_ps1):
        print(f"Ejecutando script PowerShell de instalación: {install_ps1}")
        subprocess.run(["powershell", "-File", install_ps1])
    else:
        print("No se encontró script de instalación específico. Ejecutando instalador general del ecosistema...")
        general_install = os.path.join(INSTALLATION_DIR, "install.py")
        if os.path.exists(general_install):
            subprocess.run([sys.executable, general_install])

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
    
    target_docs = []
    if "Agente" in resource_type:
        target_docs = [
            os.path.join(INSTRUCTIONS_DIR, "gemini", "docs", "AGENTS_CATALOG.md"),
            os.path.join(INSTRUCTIONS_DIR, "openai", "docs", "AGENTS_CATALOG.md"),
            os.path.join(INSTRUCTIONS_DIR, "copilot", "docs", "AGENTS_CATALOG.md")
        ]
    elif "Herramienta" in resource_type or "Framework" in resource_type or "MCP" in resource_type:
        target_docs = [
            os.path.join(INSTRUCTIONS_DIR, "gemini", "docs", "TOOLING_AND_VALIDATION.md"),
            os.path.join(INSTRUCTIONS_DIR, "openai", "docs", "TOOLING_AND_VALIDATION.md"),
            os.path.join(INSTRUCTIONS_DIR, "copilot", "docs", "TOOLING_AND_VALIDATION.md")
        ]
    elif "Skill" in resource_type:
        target_docs = [
            os.path.join(INSTRUCTIONS_DIR, "gemini", "docs", "TOOLING_AND_VALIDATION.md"),
            os.path.join(INSTRUCTIONS_DIR, "openai", "docs", "TOOLING_AND_VALIDATION.md"),
            os.path.join(INSTRUCTIONS_DIR, "copilot", "docs", "TOOLING_AND_VALIDATION.md")
        ]
    else:
        target_docs = [
            os.path.join(INSTRUCTIONS_DIR, "gemini", "sub-rules", "sub-rules-sdlc.md"),
            os.path.join(INSTRUCTIONS_DIR, "openai", "sub-rules", "sub-rules-sdlc.md")
        ]

    for doc_path in target_docs:
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Añadir el bloque generado por IA al final del documento de forma estructurada
            content += f"\n\n{ai_block}\n"
                
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Integrado formalmente en: {os.path.relpath(doc_path, ECOSYSTEM_ROOT)}")

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
        "1": ("Agente", os.path.join(PRE_DOWNLOADED_DIR, "agents")),
        "2": ("Skill", os.path.join(PRE_DOWNLOADED_DIR, "skills")),
        "3": ("Herramienta/MCP", os.path.join(PRE_DOWNLOADED_DIR, "tools")),
        "4": ("Sub-regla", os.path.join(INSTRUCTIONS_DIR, "gemini", "sub-rules")),
        "5": ("Framework/Plugin/Prompt", os.path.join(PRE_DOWNLOADED_DIR, "tools"))
    }
    
    if choice not in types_map:
        print("❌ Opción inválida. Saliendo.")
        sys.exit(1)
        
    resource_type, target_dir = types_map[choice]
    
    name = input(f"\nIntroduce el nombre/identificador del {resource_type} (ej. 'mcp-sequential-thinking'): ").strip()
    if not name:
        print("❌ El nombre no puede estar vacío.")
        sys.exit(1)
        
    resource_path = os.path.join(target_dir, name)
    exists = os.path.exists(resource_path)
    
    if exists:
        print(f"\n⚠️ [AVISO] El {resource_type} '{name}' YA EXISTE en '{resource_path}'.")
        proceed = input("¿Deseas actualizarlo y re-ejecutar su instalación? (s/N): ").strip().lower()
        if proceed != 's':
            print("Operación cancelada por el usuario.")
            sys.exit(0)
    else:
        print(f"\n✅ El {resource_type} '{name}' no existe previamente. Creando directorio...")
        os.makedirs(resource_path, exist_ok=True)
        
    # Integración con generación por IA
    integrate_into_instructions(resource_type, name)
    
    # Ejecutar script de instalación
    run_installation_script(resource_path)
    
    print(f"\n✨ ¡Ecosistema actualizado, integrado con IA e instalado con éxito para '{name}'!")

if __name__ == "__main__":
    main()
