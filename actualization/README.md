# Actualización del Ecosistema OmniAgent (`actualization/`)

Esta carpeta contiene las guías y herramientas automatizadas para añadir nuevos componentes (agentes, habilidades, herramientas o reglas) al ecosistema de orquestación de OmniAgent.

## Flujo de Actualización Interactivo
Ejecuta el script automatizado para añadir componentes de forma guiada:
```bash
python actualization/update_ecosystem.py
```

El script realiza las siguientes comprobaciones:
1. **Pregunta el tipo de recurso** a añadir (Agente, Skill, Herramienta, Sub-regla).
2. **Solicita el nombre y categoría** del recurso.
3. **Verifica duplicados**: Comprueba si ya existe en el ecosistema y te avisa antes de continuar.
4. **Actualiza automáticamente** los catálogos y referencias en `orchestration/instructions/`.
