# planner/executive_report_ai.py

from planner.models import Project
from planner.utils import load_config
from planner.risk_analysis import classify_all_projects
from openai import OpenAI
import pandas as pd

def prepare_portfolio_summary(projects):
    total_projects = len(projects)
    total_monto = sum([p.monto_autorizado for p in projects if pd.notna(p.monto_autorizado)])
    promedio_dias = (
        sum([p.dias_totales_programado for p in projects if pd.notna(p.dias_totales_programado)]) / total_projects
        if total_projects > 0 else 0
    )

    # Proyecto más caro y más retrasado (por desviación promedio)
    def deviation(project):
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
                total_diff += abs((real - plan).days)
                count += 1
        return total_diff / count if count > 0 else 0

    proyecto_caro = max(projects, key=lambda p: p.monto_autorizado if pd.notna(p.monto_autorizado) else 0)
    proyecto_retrasado = max(projects, key=lambda p: deviation(p))

    # Distribución de riesgos
    risks = classify_all_projects(projects)
    counts = {"Alto": 0, "Medio": 0, "Bajo": 0}
    for _, _, riesgo in risks:
        counts[riesgo] += 1

    return {
        "Total proyectos": total_projects,
        "Monto total": total_monto,
        "Días promedio programados": promedio_dias,
        "Proyecto más caro": f"{proyecto_caro.nombre_proyecto} (${proyecto_caro.monto_autorizado:,.2f})",
        "Proyecto más retrasado": f"{proyecto_retrasado.nombre_proyecto}",
        "Riesgos": counts
    }

def generate_executive_report(manager):
    print("\n===== GENERANDO REPORTE EJECUTIVO DEL PORTAFOLIO =====")
    projects = manager.get_projects()
    summary = prepare_portfolio_summary(projects)

    # Generar prompt para IA
    risk_text = f"Alto: {summary['Riesgos']['Alto']}, Medio: {summary['Riesgos']['Medio']}, Bajo: {summary['Riesgos']['Bajo']}"
    prompt = f"""
Eres un consultor experto en dirección de proyectos de construcción.

Genera un informe ejecutivo para la dirección general a partir del siguiente resumen del portafolio actual:

- Total proyectos: {summary['Total proyectos']}
- Monto total: ${summary['Monto total']:,.2f}
- Días promedio programados: {summary['Días promedio programados']:.2f}
- Proyecto más caro: {summary['Proyecto más caro']}
- Proyecto más retrasado: {summary['Proyecto más retrasado']}
- Distribución de riesgos: {risk_text}

Incluye:
1. Un resumen ejecutivo del estado actual.
2. Principales áreas de atención.
3. Recomendaciones estratégicas para mejorar la ejecución y mitigar riesgos.

Escribe de forma profesional, breve y clara.
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un consultor senior redactor de informes ejecutivos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    report_text = response.choices[0].message.content
    print("\n===== REPORTE EJECUTIVO IA =====")
    print(report_text)
