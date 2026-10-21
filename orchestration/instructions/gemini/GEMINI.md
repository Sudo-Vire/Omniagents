# Contexto del Proyecto y Reglas de Desarrollo

## 1. Stack Tecnológico y Arquitectura (OmniAgent)
OmniAgent es un ecosistema autónomo y multi-modelo estructurado en 3 módulos independientes:
- **Lenguaje / Framework:** Python 3.10+, Node.js / TypeScript, Cross-platform CLI.
- **Módulos Principales:**
  - `installation/`: Instaladores autónomos e independientes que descargan herramientas de fuentes oficiales.
  - `pre-downloaded/`: Catálogos de agentes (`agency-agents`, `claude-subagents`), habilidades (`skills/` incluyendo Strix y Graphify) y herramientas (`tools/`).
  - `orchestration/`: Instrucciones de orquestación multi-agente para Claude, Copilot, Gemini, OpenAI y otros modelos.

## 2. Comandos de Verificación (Esencial para agentes Gemini)
Gemini utiliza estas instrucciones para comprobar y compilar el proyecto de forma autónoma:
- **Instalación:** `python install.py` (o `python -m pip install -r installation/requirements.txt`)
- **Compilación / Sintaxis:** `python -m py_compile tools/*.py installation/*.py`
- **Pruebas:** `pytest`
- **Linter / Formato:** `ruff check .` y `biome check .`

## 3. Directrices de Estilo y Rigidez (Simulación de Temperatura Baja)
- **Filosofía Lazy Senior Dev / Ponytail:** YAGNI (el mejor código es el que no se escribe), cambios mínimos, quirúrgicos y orientados a la raíz del problema.
- **Protocolo de Comportamiento:**
  1. Pensar en voz alta antes de actuar.
  2. Presentar el plan de la fase actual.
  3. Solicitar confirmación explícita: *“¿Es correcto o deseas realizar algún cambio?”*.
  4. Esperar la aprobación del usuario antes de ejecutar cambios.
  5. Ejecutar únicamente tras recibir confirmación.
- Utiliza siempre tipado explícito y sigue la arquitectura de carpetas existente.

## 4. Gestión de Dependencias y Seguridad
- No inventes librerías ni paquetes que no existan en el ecosistema oficial.
- Si necesitas una nueva dependencia, pregúntame antes de instalarla.
- Nunca escribas credenciales, tokens o claves API en el código; utiliza variables de entorno en `.env`.

---

## 5. Módulos de Instrucciones Avanzadas (Modularización con `@file`)
Para mantener el contexto limpio y estructurado, Gemini importará automáticamente los subarchivos correspondientes:
- @./sub-rules-sdlc.md
- @./sub-rules-ecosystem.md
- @./sub-rules-superpowers.md
