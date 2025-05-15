# planner/visualizations.py

import matplotlib.pyplot as plt
from planner.models import Project
from typing import List
import pandas as pd

def plot_gantt(projects: List[Project]):
    # Filtrar proyectos con fechas
    data = [
        (p.nombre_proyecto, p.fecha_inicio, p.fecha_conclusion, p.fecha_inicio_real, p.fecha_conclusion_real)
        for p in projects
        if pd.notna(p.fecha_inicio) and pd.notna(p.fecha_conclusion)
    ]

    if not data:
        print("No hay proyectos con fechas suficientes para el Gantt.")
        return

    fig, ax = plt.subplots()
    for i, (name, start, end, real_start, real_end) in enumerate(data):
        ax.barh(i, (end - start).days, left=start, color='skyblue', label='Planificado' if i == 0 else "")
        if pd.notna(real_start) and pd.notna(real_end):
            ax.barh(i, (real_end - real_start).days, left=real_start, color='orange', label='Real' if i == 0 else "")
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([name for name, *_ in data])
    ax.set_xlabel('Fecha')
    ax.set_title('Gráfico Gantt de Proyectos')
    plt.legend()
    plt.show()

def plot_resources(projects: List[Project]):
    names = [p.nombre_proyecto for p in projects if pd.notna(p.monto_autorizado)]
    costs = [p.monto_autorizado for p in projects if pd.notna(p.monto_autorizado)]
    if not names:
        print("No hay datos de costos para graficar.")
        return
    plt.figure()
    plt.barh(names, costs)
    plt.xlabel('Monto autorizado ($)')
    plt.title('Distribución de Recursos (Costos)')
    plt.show()

def plot_complexity(projects: List[Project]):
    categories = ['Sencillo', 'Intermedio', 'Complejo', 'Extracomplejo']
    counts = {'Sencillo': 0, 'Intermedio': 0, 'Complejo': 0, 'Extracomplejo': 0}
    for p in projects:
        c = p.complejidad_obra or ''
        if 'Sencillo' in c:
            counts['Sencillo'] += 1
        elif 'Intermedio' in c:
            counts['Intermedio'] += 1
        elif 'Complejo' in c:
            counts['Complejo'] += 1
        else:
            counts['Extracomplejo'] += 1
    plt.figure()
    plt.pie(counts.values(), labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Complejidad de Proyectos')
    plt.show()

def plot_gantt_individual(project: Project):
    etapas = [
        ("RU", project.fecha_ru, project.fecha_ru_real),
        ("ADC", project.fecha_adc, project.fecha_adc_real),
        ("DB1/DB2", project.fecha_db1_db2, project.fecha_db1_db2_real),
        ("Autorización DB1/DB2", project.fecha_autorizacion_db1_db2, project.fecha_autorizacion_db1_db2_real),
        ("Licitación", project.fecha_licitacion_proveedor, project.fecha_licitacion_proveedor_real),
        ("Adjudicación", project.fecha_adjudicacion, project.fecha_adjudicacion_real),
        ("Contrato Proceso", project.fecha_contrato_proceso, project.fecha_contrato_proceso_real),
        ("Contrato Liberado", project.fecha_contrato_liberado, project.fecha_contrato_liberado_real),
        ("Inicio Ejecución", project.fecha_inicio, project.fecha_inicio_real),
        ("Conclusión", project.fecha_conclusion, project.fecha_conclusion_real),
    ]

    etapas_validas = [e for e in etapas if pd.notna(e[1]) or pd.notna(e[2])]

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (nombre, plan, real) in enumerate(etapas_validas):
        if pd.notna(plan):
            ax.plot([plan, plan], [i - 0.2, i + 0.2], color='blue', linewidth=5, label='Planeado' if i == 0 else "")
        if pd.notna(real):
            ax.plot([real, real], [i - 0.2, i + 0.2], color='orange', linewidth=5, label='Real' if i == 0 else "")

    ax.set_yticks(range(len(etapas_validas)))
    ax.set_yticklabels([e[0] for e in etapas_validas])
    ax.set_xlabel('Fecha')
    ax.set_title(f'Gantt Individual: {project.nombre_proyecto}')
    ax.legend()
    plt.show()
