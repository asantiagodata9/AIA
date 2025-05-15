# planner/predictive_risk_ai.py

from planner.models import Project
from planner.utils import load_config
from openai import OpenAI
import pandas as pd

def calculate_deviation(project):
    etapas = [
        (project.fecha_ru, project.fecha_ru_real),
        (project.fecha_adc, project.fecha_adc_real),
        (project.fecha_db1_db2, project.fecha_db1_db2_real),
        (project.fecha_autorizacion_db1_db2, project.fecha_autorizacion_db1_db2_real),
        (project.fecha_licitacion_proveedor, project.fecha_licitacion_proveedor_real),
        (project.fecha_adjudicacion, project.fecha_adjudicacion_real),
        (project.fecha_contrato_proceso, project.fecha_contrato_proceso_real),
        (project.fecha_contrato_liberado, project.fecha_contrato_liberado_real),
        (project.fecha_inicio, project.fecha_inicio_real),
        (project.fecha_conclusion, project.fecha_conclusion_real)
    ]
    total_diff = 0
    count = 0
    for plan, real in etapas:
        if pd.notna(plan) and pd.notna(real):
            diff = (real - plan).days
            total_diff += abs(diff)
            count += 1
    return total_diff / count if count > 0 else 0

def prepare_project_summary(project):
    deviation = calculate_deviation(project)
    return {
        "ID RE": project.id_re,
        "Nombre": project.nombre_proyecto,
        "Desviacion promedio (días)": deviation,
        "Complejidad": project.complejidad_obra,
        "Licencia": project.necesita_licencia,
        "Puntaje ADC": project.puntaje_adc
    }

def predictive_risk_analysis(manager):
    print("\n===== ANÁLISIS PREDICTIVO DE RIESGO (IA) =====")
    projects = manager.get_projects()
    dataset = [prepare_project_summary(p) for p in projects]
    df = pd.DataFrame(dataset)

    # Generar prompt para IA
    data_text = df.to_string(index=False)
    prompt = f"""
Eres un experto en gestión de proyectos de construcción.  
Con base en las siguientes variables por proyecto:

- Desviacion promedio (días)
- Complejidad (baja, intermedia, compleja, extracompleja)
- Licencia (sí / no)
- Puntaje ADC (0-100)

Predice la probabilidad de retraso de cada proyecto como:

- Baja (<30%)
- Media (30-70%)
- Alta (>70%)

Recomienda acciones para mitigar el riesgo en los casos medios y altos.  
Devuelve una tabla con las siguientes columnas:

ID RE | Nombre | Probabilidad de retraso | Recomendaciones

Datos de proyectos:
{data_text}
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un consultor senior de gestión de riesgos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print("\n===== PREDICCIÓN DE RIESGO =====")
    print(result_text)
