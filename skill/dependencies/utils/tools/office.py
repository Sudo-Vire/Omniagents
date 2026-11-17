import os
import sys
import argparse
import os
import sys
from pathlib import Path

# Configurar Omniroute local en localhost:20128
os.environ["OPENAI_API_BASE"] = os.getenv("OMNIROUTE_API_BASE", "http://localhost:20128/v1")
os.environ["OPENAI_API_KEY"] = os.getenv("OMNIROUTE_API_KEY", "not-needed")
os.environ["CREWAI_TRACING_ENABLED"] = "false"

model_name = "openai/antigravity/gemini-3.1-flash-lite"
project_dir = os.getcwd()

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


def collect_project_context(target_dir):
    project_files_summary = []
    key_files = ["index.html", "package.json", "README.md", "main.py", "app.py", "App.tsx", "App.jsx"]

    for filename in os.listdir(target_dir):
        if filename in key_files or filename.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".md")):
            filepath = os.path.join(target_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read(2000)
                        project_files_summary.append(f"--- Archivo: {filename} ---\n{content}\n")
                except Exception:
                    pass

    context = "\n".join(project_files_summary[:10])
    return context or "No se encontraron archivos estándar en este directorio."


def run_crewai_engine(project_dir, project_context):
    """Ejecución utilizando el motor CrewAI (conservado para compatibilidad y flujos de roles)."""
    try:
        from crewai import Agent, Crew, Process, Task
    except ImportError:
        print("[ERROR] CrewAI no está instalado. Instálalo con `pip install crewai` para usar --engine crewai.", file=sys.stderr)
        sys.exit(1)

    print(f"## Analizando proyecto en: {project_dir} con Ecosistema Dual (agency-agents + claude-subagents + CrewAI + Strix + Aider) ##")

    arch_prompt = load_prompt(agency_agents_dir, "engineering/engineering-software-architect.md", "Eres un Arquitecto de Software Senior.")
    ui_prompt = load_prompt(agency_agents_dir, "design/design-ui-designer.md", "Eres un Diseñador UI/UX experto.")
    sec_prompt = load_prompt(agency_agents_dir, "engineering/engineering-identity-access-engineer.md", "Eres un Especialista en Seguridad y OWASP.")

    tactical_prompt = "Eres un especialista técnico táctico."
    if os.path.exists(os.path.join(project_dir, "package.json")):
        tactical_prompt = load_prompt(claude_subagents_dir, "01-core-development/fullstack-developer.md", tactical_prompt)
    elif os.path.exists(os.path.join(project_dir, "requirements.txt")) or os.path.exists(os.path.join(project_dir, "pyproject.toml")):
        tactical_prompt = load_prompt(claude_subagents_dir, "02-language-specialists/django-developer.md", tactical_prompt)

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

    print('## Oficina Virtual Ecosistema Dual (agency-agents + claude-subagents + CrewAI) Iniciada ##')
    try:
        result = agency_crew.kickoff()
        print('\n================ RESULTADO DEL ECOSISTEMA DUAL (CrewAI) ================\n')
        print(result)

        output_path = os.path.join(project_dir, "OFFICE_RESULT.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(result))
        print(f"\n[OK] Informe descriptivo unificado guardado en {output_path}")
        return str(result)
    except Exception as e:
        print('Error en la ejecución unificada de CrewAI:', e, file=sys.stderr)
        raise


def run_langgraph_engine(project_dir, project_context, objective, thread_id="office-session-001", approve=True):
    """Ejecución utilizando el runtime determinista de grafos y observabilidad con LangGraph y LangSmith."""
    print(f"## Analizando proyecto en: {project_dir} con Ecosistema Dual (agency-agents + claude-subagents + LangGraph + Strix + Aider) ##")

    # Importar helper del runtime LangGraph
    # Resolver rutas relativas para importación
    tool_dir = Path(__file__).resolve()
    for parent in (tool_dir.parents[3], tool_dir.parents[4]):
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))

    try:
        from skill.framework.runtime.graph import run_orchestration
    except ImportError:
        from framework.runtime.graph import run_orchestration

    input_data = {
        "objective": objective,
        "context": project_context,
        "human_approved": approve,
        "constraints": ["OWASP Top 10 compliance", "WCAG accessibility guidelines"],
        "acceptance_criteria": ["Generar OFFICE_RESULT.md", "Validación linter limpia"],
    }

    result = run_orchestration(input_data=input_data, thread_id=thread_id)
    print('\n================ RESULTADO DEL ECOSISTEMA DUAL (LangGraph) ================\n')
    print(f"Status: {result.get('status')}")
    print(f"Result: {result.get('result')}")

    output_path = os.path.join(project_dir, "OFFICE_RESULT.md")
    office_plan = result.get("state", {}).get("office_plan")
    if office_plan:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(office_plan)
        print(f"\n[OK] Informe descriptivo unificado guardado en {output_path}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Herramienta Office Multi-Engine (LangGraph / CrewAI)")
    parser.add_argument(
        "--engine",
        choices=["langgraph", "crewai"],
        default="langgraph",
        help="Motor de ejecución para la oficina virtual: 'langgraph' (predeterminado, determinista) o 'crewai' (roles autónomos).",
    )
    parser.add_argument(
        "--objective",
        default="Análisis y planificación de arquitectura, UI y seguridad para el proyecto",
        help="Objetivo de la planificación en la oficina virtual.",
    )
    parser.add_argument(
        "--thread-id",
        default="office-session-001",
        help="Identificador de hilo para checkpointing y observabilidad LangSmith.",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        default=True,
        help="Aprobar automáticamente el plan de ejecución en la compuerta humana.",
    )

    args = parser.parse_args()
    context = collect_project_context(project_dir)

    if args.engine == "crewai":
        run_crewai_engine(project_dir, context)
    else:
        run_langgraph_engine(
            project_dir=project_dir,
            project_context=context,
            objective=args.objective,
            thread_id=args.thread_id,
            approve=args.approve,
        )


if __name__ == '__main__':
    main()

