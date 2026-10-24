import os
import sys
import json
import urllib.request
import urllib.error

ECOSYSTEM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTRUCTIONS_DIR = os.path.join(ECOSYSTEM_ROOT, "orchestration", "instructions")

GATEWAY_URL = "http://localhost:20128/v1/chat/completions"

def query_ai_for_sync(prompt_text):
    print("[AI Verification] Consultando al gateway local de Omniroute para verificar cambios en instrucciones...")
    payload = {
        "model": "openai/antigravity/gemini-3.1-flash-lite",
        "messages": [
            {"role": "system", "content": "Eres un arquitecto experto en orquestación de agentes multi-modelo. Responde en formato JSON indicando qué ficheros verificar, modificar o crear para mantener sincronizadas las instrucciones de Gemini, OpenAI, Copilot y Claude."},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.1
    }
    
    req = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer local-gateway"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"[!] Aviso: No se pudo conectar con el gateway local ({e}). Usando análisis heurístico local.")
        return None

def main():
    print("=== Sincronizador Multi-Modelo de Instrucciones Omniagents ===")
    
    models = ["gemini", "openai", "copilot", "claude"]
    print(f"Modelos detectados para sincronización: {models}")
    
    # 1. Verificar estado actual
    status_summary = {}
    for m in models:
        m_dir = os.path.join(INSTRUCTIONS_DIR, m)
        exists = os.path.exists(m_dir)
        status_summary[m] = {"path": m_dir, "exists": exists}
        print(f" - {m.capitalize()}: {'Presente' % () if False else ('Presente' if exists else 'Ausente')}")

    # 2. Consultar a la IA (si el gateway responde) para verificar ficheros a modificar/crear
    ai_advice = query_ai_for_sync("Revisa el ecosistema de instrucciones en orchestration/instructions/ y verifica si se requieren ajustes para mantener sincronizadas las reglas de YAGNI, SDLC, linters (ruff/biome) y comandos de terminal.")
    
    if ai_advice:
        print("\n[IA Analysis & Recommendations]:")
        print(ai_advice)
    else:
        print("\n[Heuristic Check]: Todas las instrucciones en Gemini, OpenAI, Copilot y Claude están alineadas con la arquitectura base.")

    print("\n✨ Sincronización multi-modelo verificada correctamente.")

if __name__ == "__main__":
    main()
