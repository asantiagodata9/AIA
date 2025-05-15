# reporting_agent.py

from planner.utils import load_config
from openai import OpenAI

def generate_simple_report(projects):
    print("\n===== REPORTING AGENT =====")
    resumen = f"Total proyectos: {len(projects)}\n"
    resumen += "\n".join([f"{p.id_re} | {p.nombre_proyecto} | {p.etapa}" for p in projects])

    prompt = f"""
Eres un agente de reporting ejecutivo. A partir del siguiente estado de proyectos:
{resumen}
Escribe un breve informe para la Dirección General.
Incluye:
- Estado general
- Principales riesgos o demoras
- Recomendaciones generales
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Eres un reporting agent."},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )

    print(response.choices[0].message.content)
