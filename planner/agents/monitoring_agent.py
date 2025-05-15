# monitoring_agent.py

from planner.utils import load_config
from openai import OpenAI

def monitor_progress(projects):
    print("\n===== MONITORING AGENT =====")
    summary = f"Total proyectos: {len(projects)}\n"
    for p in projects:
        summary += f"{p.id_re} | {p.nombre_proyecto} | Etapa actual: {p.etapa}\n"

    prompt = f"""
Eres un agente de seguimiento. Analiza el estado actual de los proyectos:
{summary}
Responde:
- ¿Qué proyectos parecen estar detenidos?
- ¿Qué recomendaciones das para reactivar los flujos?
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Eres un agente de monitoreo."},
                  {"role": "user", "content": prompt}],
        temperature=0.2
    )

    print(response.choices[0].message.content)
