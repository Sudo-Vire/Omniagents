# Core Architecture & Technical Stack

## 1. Technical Stack & Repository Structure
- **Backend/Scripts**: Python (Ruff formatting/linting).
- **Frontend/Web**: TypeScript/JavaScript, HTML/CSS (Biome checking).
- **Local Inference Gateway**: Omniroute (`http://localhost:20128/v1`).
- **Knowledge Graph**: Graphify (`graphify query "<question>"`).

## 2. Architectural Knowledge Graph (Graphify)
For any question about architecture, file relationships, dependencies or component explanation:
- **When to use**: When questions of the type *"how do I..."*, *"where is..."*, *"what does..."* or *"explain architecture"* are asked.
- **Tool**: `graphify query "<question>"` or review `graphify-out/GRAPH_REPORT.md` and `graphify-out/wiki/index.md`.
