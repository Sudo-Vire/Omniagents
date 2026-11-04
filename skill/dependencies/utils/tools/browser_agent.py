import os
import sys
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent

# Configurar Omniroute local en localhost:20128
os.environ["OPENAI_API_BASE"] = os.getenv("OMNIROUTE_API_BASE", "http://localhost:20128/v1")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "not-needed")

# Usar ChatOpenAI con Omniroute para browser-use
llm = ChatOpenAI(
    model="openai/antigravity/gemini-3.1-flash-lite",
    openai_api_base="http://localhost:20128/v1",
    openai_api_key="not-needed"
)

async def run_browser_task(task_description: str):
    agent = Agent(
        task=task_description,
        llm=llm
    )
    result = await agent.run()
    print("Resultado del Agente Web:", result)

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Navega por la página web actual, verifica elementos y prueba la interfaz visualmente."
    print(f"## Ejecutando Agente Web Autónomo (Browser-Use) con tarea: {task} ##")
    asyncio.run(run_browser_task(task))
