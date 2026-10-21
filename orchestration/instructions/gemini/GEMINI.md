# Google Gemini Master Agent Instructions (GEMINI.md)

## 1. Contexto del Proyecto y Reglas de Desarrollo
Este archivo establece las directrices permanentes para los modelos y agentes Google Gemini operando dentro de OmniAgent.
- **Filosofía Operativa (Lazy Senior Dev / Ponytail)**: YAGNI, cambios mínimos, quirúrgicos y orientados a la raíz del problema.
- **Protocolo de Comportamiento Obligatorio**:
  1. Pensar en voz alta antes de actuar.
  2. Presentar el plan de la fase actual.
  3. Solicitar confirmación explícita: *“¿Es correcto o deseas realizar algún cambio?”*.
  4. Esperar la aprobación del usuario antes de ejecutar cambios.
  5. Ejecutar únicamente tras recibir confirmación.

## 2. Comandos de Verificación (Esencial para agentes Gemini)
Gemini utiliza estas instrucciones para comprobar la validez de su código:
- **Comando de instalación:** `python -m pip install -r installation/requirements.txt` (o `npm install`)
- **Comando de pruebas:** `pytest` / `npm test`
- **Comando de compilación:** `python -m py_compile tools/*.py installation/*.py` / `npm run build`
- **Comando de linter:** `ruff check .` / `biome check .`

## 3. Restricciones y Seguridad
- Nunca expongas credenciales ni claves API de entorno (respalda siempre con variables de entorno o `.env`).
- Respeta la separación estricta de los 3 módulos del proyecto: `installation/` (descargas oficiales independientes), `pre-downloaded/` (activos locales), y `orchestration/` (instrucciones multi-agente).

## 4. Características avanzadas de Gemini compatibles
- **Modularización con `@file`**: Puedes importar contextos adicionales escribiendo referencias como `@./orchestration/instructions/gemini/gemini-config.json`.
- **Jerarquía Ascendente**: Gemini fusiona inteligentemente contextos globales (`~/.gemini/GEMINI.md`) con el `GEMINI.md` raíz de este repositorio.

## 5. Catálogo Dual y Metodología de Ejecución (Master Rulebook)
- **Fase 0 – Descubrimiento y Verificación**: Inspección con herramientas de código antes de proponer cambios.
- **Fase 1 – Implementación Quirúrgica**: Cambios limpios y completos.
- **Fase 2 – Verificación y Validación**: Pruebas y linters obligatorios.
- **Ecosistema Dual**: Integración de macro-agentes (`agency-agents`), micro-subagentes (`claude-subagents`), habilidades (`skills/` incluyendo Strix y Graphify), y pasarela local Omniroute en `http://localhost:20128/v1`.
