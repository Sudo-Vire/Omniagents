# Actualización del Ecosistema OmniAgent (`framework/actualization/`)

Esta carpeta contiene las guías y herramientas automatizadas para añadir nuevos componentes (agentes, habilidades, herramientas o reglas) al ecosistema de orquestación de OmniAgent.

## Flujo de Actualización Interactivo
Desde la carpeta raíz de la skill (donde está `SKILL.md`), ejecuta el script automatizado para añadir componentes de forma guiada:
```bash
python framework/actualization/update_ecosystem.py
```
Para sincronizar las instrucciones entre modelos, consulta [MODEL_SYNC_INSTRUCTIONS.md](./MODEL_SYNC_INSTRUCTIONS.md); el protocolo para asistentes está en [ACTUALIZATION.md](./ACTUALIZATION.md). El inventario que se mantiene está en [check_utils.txt](../../dependencies/utils/check_utils.txt) y las instrucciones actualizadas en [orchestration](../orchestration/README.md).

El script realiza las siguientes comprobaciones:
1. **Pregunta el tipo de recurso** a añadir (Agente, Skill, Herramienta, Sub-regla).
2. **Solicita el nombre y categoría** del recurso.
3. **Verifica duplicados**: Comprueba si ya existe en el ecosistema y te avisa antes de continuar.
4. **Actualiza automáticamente** los catálogos y referencias de cada modelo (Gemini, OpenAI, Copilot, Claude y others) en `framework/orchestration/instructions/`.

Los agentes, skills, herramientas y recursos de framework/plugin/prompt se anotan en `dependencies/utils/check_utils.txt`. Después de incorporar el contenido descargado, ejecuta `python scripts/check_dependencies.py` desde `skill/` para validar el inventario.
