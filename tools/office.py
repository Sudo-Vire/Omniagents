import os
import sys
from crewai import Agent, Crew, Process, Task

# Configurar Omniroute local en localhost:20128
os.environ["OPENAI_API_BASE"] = os.getenv("OMNIROUTE_API_BASE", "http://localhost:20128/v1")
os.environ["OPENAI_API_KEY"] = os.getenv("OMNIROUTE_API_KEY", "not-needed")
os.environ["CREWAI_TRACING_ENABLED"] = "false"

model_name = "openai/antigravity/gemini-3.1-flash-lite"

project_dir = os.getcwd()
print(f"## Analizando proyecto en: {project_dir} con Ecosistema Dual (agency-agents + claude-subagents + CrewAI + Strix + Aider) ##")

# Rutas genéricas basadas en el directorio home del usuario actual (~/IA)
home_dir = os.path.expanduser("~")
ia_dir = os.getenv("IA_DIR", os.path.join(home_dir, "IA"))
agency_agents_dir = os.path.join(ia_dir, "agency-agents")
claude_subagents_dir = os.path.join(ia_dir, "claude-subagents", "categories")

def load_prompt(base_dir, rel_path, default_fallback):
    path = os.path.join(base_dir, rel_path)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()[:1500]
        except Exception:
            pass
    return default_fallback

# Cargar roles macro de agency-agents
arch_prompt = load_prompt(agency_agents_dir, "engineering/engineering-software-architect.md", "Eres un Arquitecto de Software Senior.")
ui_prompt = load_prompt(agency_agents_dir, "design/design-ui-designer.md", "Eres un Diseñador UI/UX experto.")
sec_prompt = load_prompt(agency_agents_dir, "engineering/engineering-identity-access-engineer.md", "Eres un Especialista en Seguridad y OWASP.")
dev_prompt = load_prompt(agency_agents_dir, "engineering/engineering-senior-developer.md", "Eres un Desarrollador Senior.")

# Detectar tecnología específica para cargar micro-subagente de claude-subagents si aplica
tactical_prompt = "Eres un especialista técnico táctico."
if os.path.exists(os.path.join(project_dir, "package.json")):
    tactical_prompt = load_prompt(claude_subagents_dir, "01-core-development/fullstack-developer.md", tactical_prompt)
elif os.path.exists(os.path.join(project_dir, "requirements.txt")) or os.path.exists(os.path.join(project_dir, "pyproject.toml")):
    tactical_prompt = load_prompt(claude_subagents_dir, "02-language-specialists/django-developer.md", tactical_prompt)

# Recopilar contexto del proyecto
project_files_summary = []
key_files = ["index.html", "package.json", "README.md", "main.py", "app.py", "App.tsx", "App.jsx"]

for filename in os.listdir(project_dir):
    if filename in key_files or filename.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".md")):
        filepath = os.path.join(project_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read(2000)
                    project_files_summary.append(f"--- Archivo: {filename} ---\n{content}\n")
            except Exception:
                pass

project_context = "\n".join(project_files_summary[:10])
if not project_context:
    project_context = "No se encontraron archivos estándar en este directorio."

architect_agent = Agent(
    role='Software Architect (`agency-agents/engineering/engineering-software-architect.md`)',
    goal='Diseñar la arquitectura técnica y modular del proyecto.',
    backstory=arch_prompt,
    verbose=True,
    llm=model_name
)

ui_agent = Agent(
    role='UI/UX Designer (`agency-agents/design/design-ui-designer.md`)',
    goal='Optimizar la interfaz de usuario, estética y accesibilidad WCAG.',
    backstory=ui_prompt,
    verbose=True,
    llm=model_name
)

security_agent = Agent(
    role='Security & Strix Auditor (`agency-agents/security/` + Strix)',
    goal='Auditar vulnerabilidades, OWASP Top 10 y planificar pentesting con Strix.',
    backstory=sec_prompt,
    verbose=True,
    llm=model_name
)

tactical_agent = Agent(
    role='Tactical Micro-Agent (`awesome-claude-code-subagents`)',
    goal='Aportar especificación técnica granular adaptada al stack tecnológico del proyecto.',
    backstory=tactical_prompt,
    verbose=True,
    llm=model_name
)

task_unified = Task(
    description=f"Análisis unificado del proyecto en {project_dir}:\n\n{project_context}\n\n1. Software Architect: Diseña la arquitectura general.\n2. UI/UX Designer: Revisa estética y accesibilidad.\n3. Security Auditor: Evalúa riesgos OWASP y pruebas con Strix.\n4. Tactical Micro-Agent: Aporta la capa de especialización técnica granular.\n\nIMPORTANTE para OFFICE_RESULT.md: Escribe una **descripción técnica y funcional detallada**, accesible para cualquier persona (sin código masivo, explicando el qué, el por qué y el cómo) para que luego Aider ejecute la programación.",
    expected_output='Informe unificado del ecosistema dual (agency-agents + claude-subagents) con descripción técnica y funcional accesible.',
    agent=architect_agent
)

agency_crew = Crew(
    agents=[architect_agent, ui_agent, security_agent, tactical_agent],
    tasks=[task_unified],
    process=Process.sequential,
    verbose=True
)

if __name__ == '__main__':
    print('## Oficina Virtual Ecosistema Dual (agency-agents + claude-subagents + CrewAI) Iniciada ##')
    try:
        result = agency_crew.kickoff()
        print('\n================ RESULTADO DEL ECOSISTEMA DUAL ================\n')
        print(result)
        
        output_path = os.path.join(project_dir, "OFFICE_RESULT.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(result))
        print(f"\n[OK] Informe descriptivo unificado guardado en {output_path}")
        
    except Exception as e:
        print('Error en la ejecución unificada:', e)
