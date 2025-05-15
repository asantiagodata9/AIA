# planner/risk_analysis.py

from planner.models import Project
from typing import List
import pandas as pd

def calculate_days_difference(estimated, real):
    if pd.isna(estimated) or pd.isna(real):
        return 0
    return (real - estimated).days

def classify_project_risk(project: Project) -> str:
    severity = 0

    # 1️⃣ Desviaciones en TODAS las etapas
    etapa_pairs = [
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

    for est, real in etapa_pairs:
        diff = abs(calculate_days_difference(est, real))
        if diff > 30:
            severity += 2
        elif diff > 10:
            severity += 1

    # 2️⃣ Puntaje ADC
    if pd.notna(project.puntaje_adc):
        if project.puntaje_adc >= 90:
            severity -= 0.5  # mejora
        elif project.puntaje_adc < 70:
            severity += 0.5  # empeora

    # 3️⃣ Complejidad obra
    if project.complejidad_obra:
        comp = project.complejidad_obra.lower()
        if "complejo" in comp:
            severity += 1
        elif "intermedio" in comp:
            severity += 0.5

    # 4️⃣ Licencia
    if project.necesita_licencia and "sí" in str(project.necesita_licencia).lower():
        severity += 1

    # Clasificación final
    if severity >= 3:
        return "Alto"
    elif severity >= 1.5:
        return "Medio"
    else:
        return "Bajo"

def classify_all_projects(projects: List[Project]) -> List[tuple]:
    results = []
    for project in projects:
        risk = classify_project_risk(project)
        results.append((project.id_re, project.nombre_proyecto, risk))
    return results
