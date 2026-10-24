# Agentic Instructions: Cross-Model Instruction Sync (`actualization/`)

Cuando el usuario solicite actualizar las instrucciones de todos los agentes según su modelo específico, el asistente agéntico debe seguir este protocolo guiado por IA:

1. **Escaneo de Modelos**: El script analiza las carpetas de instrucciones en `orchestration/instructions/` (Gemini, OpenAI, Copilot, Claude).
2. **Verificación Inteligente (IA / Omniroute Gateway)**:
   - El script consulta el gateway local (`http://localhost:20128/v1`) para analizar la coherencia y proponer las modificaciones o creaciones de ficheros necesarias para cada runtime.
3. **Optimización por Modelo**:
   - **Gemini**: Markdown puro, command-driven, `@file` modular y caché de contexto.
   - **OpenAI**: Markdown puro, Assistants API (`assistant-instructions.json`) y submódulos.
   - **Copilot**: Instrucciones nativas de VS Code (`copilot-instructions.md`).
   - **Claude**: Estructura enriquecida con etiquetas XML y subagentes tácticos.
4. **Ejecución y Git Commit**: Aplica los cambios propuestos, ejecuta linters y commitea con la traza de autoría.

## Cómo ejecutar el sincronizador:
```bash
python actualization/update_model_instructions.py
```
