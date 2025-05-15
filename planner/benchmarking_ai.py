# planner/benchmarking_ai.py

from planner.utils import load_config
from planner.risk_analysis import classify_all_projects
from openai import OpenAI
import pandas as pd

def prepare_summary(projects):
    total_projects = len(projects)
    total_monto = sum([p.monto_autorizado for p in projects if pd.notna(p.monto_autorizado)])
    promedio_dias = (
        sum([p.dias_totales_programado for p in projects if pd.notna(p.dias_totales_programado)]) / total_projects
        if total_projects > 0 else 0
    )

    risks = classify_all_projects(projects)
    counts = {"Alto": 0, "Medio": 0, "Bajo": 0}
    for _, _, riesgo in risks:
        counts[riesgo] += 1

    return {
        "Total proyectos": total_projects,
        "Monto total": total_monto,
        "Días promedio programados": promedio_dias,
        "Riesgos": counts
    }

def benchmarking_analysis(manager):
    print("\n===== BENCHMARKING IA: COMPARACIÓN HISTÓRICA =====")
    projects_current = manager.get_projects()
    projects_historical = projects_current  # 👉 para demo usa mismo dataset

    current = prepare_summary(projects_current)
    historical = prepare_summary(projects_historical)

    # Crear prompt para IA
    current_risks = f"Alto: {current['Riesgos']['Alto']}, Medio: {current['Riesgos']['Medio']}, Bajo: {current['Riesgos']['Bajo']}"
    historical_risks = f"Alto: {historical['Riesgos']['Alto']}, Medio: {historical['Riesgos']['Medio']}, Bajo: {historical['Riesgos']['Bajo']}"

    prompt = f"""
Eres un experto en benchmarking y análisis de portafolios de proyectos de construcción.

Compara el desempeño actual contra un histórico previo.  
Datos actuales:
- Total proyectos: {current['Total proyectos']}
- Monto total: ${current['Monto total']:,.2f}
- Días promedio programados: {current['Días promedio programados']:.2f}
- Distribución de riesgos: {current_risks}

Datos históricos:
- Total proyectos: {historical['Total proyectos']}
- Monto total: ${historical['Monto total']:,.2f}
- Días promedio programados: {historical['Días promedio programados']:.2f}
- Distribución de riesgos: {historical_risks}

Escribe un informe profesional que incluya:
1. Comparación entre ambos periodos
2. Principales hallazgos
3. Recomendaciones para mejorar el desempeño futuro

Sé breve, claro y preciso para dirección general.
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un consultor de benchmarking corporativo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print(result_text)
