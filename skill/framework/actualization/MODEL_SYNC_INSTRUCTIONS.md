# Agentic Instructions: Cross-Model Instruction Sync (`actualization/`)

Cuando el usuario solicite actualizar las instrucciones de todos los agentes según su modelo específico, el asistente agéntico debe seguir este protocolo guiado por IA:

1. **Escaneo de Modelos**: El script analiza las carpetas de instrucciones en `framework/orchestration/instructions/` (Gemini, OpenAI, Copilot, Claude y others). Cada carpeta debe seguir siendo autocontenida: sus enlaces solo apuntan a archivos de la misma carpeta.
2. **Verificación Inteligente (IA / Omniroute Gateway)**:
   - El script consulta al LLM en uso para analizar la coherencia y proponer las modificaciones o creaciones de ficheros necesarias para cada runtime.
3. **Optimización por Modelo**:
   - **Gemini**: Markdown puro, command-driven, `@file` modular y caché de contexto.
   - **OpenAI**: Markdown puro, Assistants API (`assistant-instructions.json`) y submódulos.
   - **Copilot**: Instrucciones específicas de Copilot (`copilot-instructions.md`), solo cuando ese host esté en uso.
   - **Claude**: Estructura enriquecida con etiquetas XML y subagentes tácticos.
4. **Ejecución y Git**: Revisa los cambios propuestos y ejecuta las validaciones disponibles. Pide autorización antes de modificar instrucciones o crear commits.

## Cómo ejecutar el sincronizador:
```bash
python <skill-root>/framework/actualization/update_model_instructions.py
```
