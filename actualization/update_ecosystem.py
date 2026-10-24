import os
import sys

# Definición de rutas del ecosistema
ECOSYSTEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRE_DOWNLOADED_DIR = os.path.join(ECOSYSTEM_ROOT, "pre-downloaded")
ORCHESTRATION_DIR = os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions")

def main():
    print("=== Asistente de Actualización del Ecosistema OmniAgent ===")
    
    # Paso 1: Preguntar qué se quiere añadir
    print("\n¿Qué deseas añadir al ecosistema?")
    print("1. Agente (agency-agents / claude-subagents)")
    print("2. Habilidad (Skill)")
    print("3. Herramienta (Tool)")
    print("4. Sub-regla (Sub-rule)")
    
    choice = input("\nSelecciona una opción (1-4): ").strip()
    
    types_map = {
        "1": ("Agente", os.path.join(PRE_DOWNLOADED_DIR, "agents")),
        "2": ("Skill", os.path.join(PRE_DOWNLOADED_DIR, "skills")),
        "3": ("Tool", os.path.join(PRE_DOWNLOADED_DIR, "tools")),
        "4": ("Sub-rule", os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "gemini", "sub-rules"))
    }
    
    if choice not in types_map:
        print("❌ Opción inválida. Saliendo.")
        sys.exit(1)
        
    resource_type, target_dir = types_map[choice]
    
    # Paso 2: Pedir el nombre del recurso
    name = input(f"\nIntroduce el nombre/identificador del {resource_type} (ej. 'cybersecurity-auditor' o 'strix'): ").strip()
    if not name:
        print("❌ El nombre no puede estar vacío.")
        sys.exit(1)
        
    # Paso 3: Comprobar si ya existe
    # Comprobación en pre-downloaded o sub-rules
    existing_path = ""
    if choice in ["1", "2", "3"]:
        # Buscar en subcarpetas de pre-downloaded
        found = False
        for root, dirs, files in os.walk(target_dir):
            if name.lower() in [d.lower() for d in dirs] or any(name.lower() in f.lower() for f in files):
                found = True
                existing_path = root
                break
        exists = found
    else:
        file_path = os.path.join(target_dir, f"{name}.md")
        exists = os.path.exists(file_path)
        existing_path = file_path
        
    if exists:
        print(f"\n⚠️ [AVISO] El {resource_type} '{name}' YA EXISTE en el ecosistema (ubicación: {existing_path}).")
        proceed = input("¿Deseas actualizar sus referencias o sobrescribirlo de todas formas? (s/N): ").strip().lower()
        if proceed != 's':
            print("Operación cancelada por el usuario.")
            sys.exit(0)
    else:
        print(f"\n✅ El {resource_type} '{name}' no existe previamente. Procediendo con la creación y registro.")
        
    # Paso 4: Registrar en los catálogos de orquestación
    print(f"\n📝 Registrando '{name}' en los catálogos de orquestación (Gemini, OpenAI, Copilot)...")
    
    # Actualizar AGENTS_CATALOG.md en gemini y openai si es agente/skill
    catalog_paths = [
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "gemini", "docs", "AGENTS_CATALOG.md"),
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "openai", "docs", "AGENTS_CATALOG.md"),
        os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions", "copilot", "docs", "AGENTS_CATALOG.md")
    ]
    
    entry = f"\n- **Nuevo {resource_type}**: `{name}` (Añadido recientemente al ecosistema)."
    
    for cat_path in catalog_paths:
        if os.path.exists(cat_path):
            with open(cat_path, "a", encoding="utf-8") as f:
                f.write(entry)
            print(f"  -> Actualizado: {os.path.relpath(cat_path, ECOSYSTEM_ROOT)}")
            
    print(f"\n✨ ¡Actualización completada con éxito para '{name}'!")

if __name__ == "__main__":
    main()
