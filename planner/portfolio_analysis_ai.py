# planner/portfolio_analysis_ai.py

from planner.utils import load_config
from openai import OpenAI
import pandas as pd

def prepare_portfolio_data(projects):
    dataset = []
    for project in projects:
        dataset.append({
            "ID RE": project.id_re,
            "Nombre": project.nombre_proyecto,
            "Campus": project.campus_conjunto,
            "Proveedor": project.proveedor_obra,
            "Categoría": project.categoria_proyecto,
            "Monto autorizado": project.monto_autorizado,
            "Complejidad": project.complejidad_obra
        })
    return pd.DataFrame(dataset)

def portfolio_analysis(manager):
    print("\n===== ANÁLISIS ESTRATÉGICO DEL PORTAFOLIO =====")
    projects = manager.get_projects()
    df = prepare_portfolio_data(projects)

    data_text = df.to_string(index=False)
    prompt = f"""
Eres un analista estratégico experto en portafolios de proyectos de construcción.

A continuación se presenta el portafolio actual:
{data_text}

Analiza y responde:
1. ¿Existen proveedores, campus o categorías que concentren demasiado volumen de proyectos?
2. ¿Hay riesgos potenciales por falta de diversificación?
3. Proporciona recomendaciones para balancear el portafolio y reducir riesgos.

Redacta un informe profesional, breve y claro para presentar a dirección.
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asesor senior de estrategia corporativa."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print(result_text)
