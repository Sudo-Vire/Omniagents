import os
import sys
import subprocess

ECOSYSTEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRE_DOWNLOADED_DIR = os.path.join(ECOSYSTEM_ROOT, "pre-downloaded")
INSTALLATION_DIR = os.path.join(ECOSYSTEM_ROOT, "installation")

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
        print("No se encontró script de instalación específico en el recurso. Ejecutando instalador general del ecosistema...")
        general_install = os.path.join(INSTALLATION_DIR, "install.py")
        if os.path.exists(general_install):
            subprocess.run([sys.executable, general_install])

def main():
    print("=== Asistente Avanzado de Actualización del Ecosistema Omniagents ===")
    
    print("\n¿Qué deseas añadir al ecosistema?")
    print("1. Agente (agency-agents / claude-subagents)")
    print("2. Habilidad (Skill)")
    print("3. Herramienta (Tool)")
    print("4. Sub-regla / Instrucción (Sub-rule)")
    print("5. Framework / Plugin / MCP Server / Prompt")
    
    choice = input("\nSelecciona una opción (1-5): ").strip()
    
    types_map = {
        "1": ("Agente", os.path.join(PRE_DOWNLOADED_DIR, "agents")),
        "2": ("Skill", os.path.join(PRE_DOWNLOADED_DIR, "skills")),
        "3": ("Herramienta", os.path.join(PRE_DOWNLOADED_DIR, "tools")),
        "4": ("Sub-regla", os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "gemini", "sub-rules")),
        "5": ("Framework/Plugin/MCP/Prompt", os.path.join(PRE_DOWNLOADED_DIR, "tools"))
    }
    
    if choice not in types_map:
        print("❌ Opción inválida. Saliendo.")
        sys.exit(1)
        
    resource_type, target_dir = types_map[choice]
    
    name = input(f"\nIntroduce el nombre/identificador del {resource_type} (ej. 'my-new-mcp-server'): ").strip()
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
        
    # Registrar en catálogos
    catalog_paths = [
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "gemini", "docs", "AGENTS_CATALOG.md"),
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "openai", "docs", "AGENTS_CATALOG.md"),
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "copilot", "docs", "AGENTS_CATALOG.md")
    ]
    
    entry = f"\n- **Nuevo {resource_type}**: `{name}` (Añadido/Actualizado)."
    for cat_path in catalog_paths:
        if os.path.exists(cat_path):
            with open(cat_path, "a", encoding="utf-8") as f:
                f.write(entry)
            print(f"  -> Catálogo actualizado: {os.path.relpath(cat_path, ECOSYSTEM_ROOT)}")
            
    # Ejecutar script de instalación del recurso o ecosistema
    run_installation_script(resource_path)
    
    print(f"\n✨ ¡Ecosistema actualizado e instalado con éxito para '{name}'!")

if __name__ == "__main__":
    main()
