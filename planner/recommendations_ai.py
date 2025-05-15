# planner/recommendations_ai.py

from planner.utils import load_config
from openai import OpenAI
import pandas as pd

def prepare_project_summary(project):
    return {
        "ID RE": project.id_re,
        "Nombre": project.nombre_proyecto,
        "Categoría": project.categoria_proyecto,
        "Monto autorizado": project.monto_autorizado,
        "Complejidad": project.complejidad_obra,
        "Puntaje ADC": project.puntaje_adc,
        "Licencia requerida": project.necesita_licencia
    }

def recommend_for_portfolio(manager):
    print("\n===== RECOMENDACIONES IA: PORTAFOLIO =====")
    projects = manager.get_projects()
    dataset = [prepare_project_summary(p) for p in projects]
    df = pd.DataFrame(dataset)

    data_text = df.to_string(index=False)
    prompt = f"""
Eres un consultor experto en ejecución de proyectos de construcción.  
Analiza el siguiente portafolio de proyectos:

{data_text}

Para cada proyecto, sugiere recomendaciones concretas y prácticas para mejorar la ejecución:
- Considera categoría, monto, complejidad, puntaje ADC y si requiere licencia.
- Da consejos claros, útiles y ejecutivos.

Devuelve tabla: ID RE | Nombre | Recomendaciones
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un consultor senior de proyectos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print(result_text)

def recommend_for_project(project):
    print(f"\n===== RECOMENDACIONES IA: PROYECTO {project.id_re} =====")
    data = f"""
ID RE: {project.id_re}
Nombre: {project.nombre_proyecto}
Categoría: {project.categoria_proyecto}
Monto autorizado: {project.monto_autorizado}
Complejidad: {project.complejidad_obra}
Puntaje ADC: {project.puntaje_adc}
Licencia requerida: {project.necesita_licencia}
"""

    prompt = f"""
Eres un consultor experto en ejecución de proyectos de construcción.

El cliente te pide una asesoría personalizada para mejorar la ejecución de este proyecto:
{data}

Da recomendaciones concretas y accionables para acelerar y mejorar la ejecución:
- Considera todas las variables.
- Sé breve, claro y práctico.
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asesor estratégico de proyectos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print(result_text)
