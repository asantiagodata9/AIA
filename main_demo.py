# main_demo.py

import os
from planner.models import ProjectManager
from planner.evaluation import evaluate_project_with_gpt
from planner.risk_analysis import classify_all_projects
from planner.visualizations import (
    plot_gantt,
    plot_resources,
    plot_complexity,
    plot_gantt_individual
)
from planner.utils import load_config
from planner.predictive_risk_ai import predictive_risk_analysis
from planner.executive_report_ai import generate_executive_report
from planner.recommendations_ai import recommend_for_portfolio
from planner.portfolio_analysis_ai import portfolio_analysis
from planner.benchmarking_ai import benchmarking_analysis
from planner.schedule_suggestion_ai import schedule_suggestion
from planner.agents.monitoring_agent import monitor_progress
from planner.agents.alerting_agent import detect_alerts
from planner.agents.reporting_agent import generate_simple_report
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd

def report_general(manager):
    projects = manager.get_projects()
    total = len(projects)
    monto_list = [p.monto_autorizado for p in projects if pd.notna(p.monto_autorizado)]
    dias_list = [p.dias_totales_programado for p in projects if pd.notna(p.dias_totales_programado)]
    print("\n===== REPORTE GENERAL =====")
    print(f"Total proyectos: {total}")
    print(f"Monto total autorizado: ${sum(monto_list):,.2f}")
    if dias_list:
        print(f"Días promedio programados: {pd.Series(dias_list).mean():.2f}")

def consulta_proyecto(manager):
    id_re = input("👉 Ingresa el ID RE del proyecto: ").strip()
    proyecto = next((p for p in manager.get_projects() if str(p.id_re) == id_re), None)
    if proyecto:
        print(f"\n✅ Proyecto: {proyecto.nombre_proyecto}")
        print(f"Campus: {proyecto.campus_conjunto} | Etapa: {proyecto.etapa}")
        print(f"Monto: ${proyecto.monto_autorizado}")
        plot_gantt_individual(proyecto)
    else:
        print("❌ No encontrado.")

def evaluar_proyecto(manager):
    id_re = input("👉 Ingresa el ID RE del proyecto: ").strip()
    proyecto = next((p for p in manager.get_projects() if str(p.id_re) == id_re), None)
    if proyecto:
        resultado = evaluate_project_with_gpt(proyecto)
        print(resultado)
    else:
        print("❌ No encontrado.")

def clasificar_riesgo(manager):
    results = classify_all_projects(manager.get_projects())
    colors = {"Alto": "\033[91m", "Medio": "\033[93m", "Bajo": "\033[92m", "ENDC": "\033[0m"}
    risk_order = {"Alto": 0, "Medio": 1, "Bajo": 2}
    def extract_id_number(id_re):
        digits = ''.join(filter(str.isdigit, str(id_re)))
        return int(digits) if digits else 0
    results_sorted = sorted(results, key=lambda x: (risk_order.get(x[2], 3), -extract_id_number(x[0])))
    counts = {"Alto": 0, "Medio": 0, "Bajo": 0}
    for id_re, nombre, riesgo in results_sorted:
        color = colors.get(riesgo, "")
        endc = colors["ENDC"]
        print(f"{color}ID RE: {id_re} | {nombre} | Riesgo: {riesgo}{endc}")
        counts[riesgo] += 1
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors_pie = ['red', 'yellow', 'green']
    plt.figure()
    plt.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Riesgos')
    plt.show()

def mostrar_graficas(manager):
    projects = manager.get_projects()
    plot_gantt(projects)
    plot_resources(projects)
    plot_complexity(projects)

def route_instruction_to_action(user_input):
    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])

    prompt = f"""
Eres un asistente IA de planificación. Estas son las opciones:

1 → Reporte general
2 → Consulta proyecto
3 → Evaluar proyecto IA
4 → Clasificación de riesgos
5 → Mostrar gráficas
6 → Análisis riesgo predictivo IA
7 → Reporte ejecutivo IA
8 → Recomendaciones IA
9 → Análisis portafolio IA
10 → Benchmarking histórico
11 → Sugerir cronograma ideal
12 → Monitoring Agent
13 → Alerting Agent
14 → Reporting Agent
15 → LAB IA (todos los agentes juntos)

El usuario dijo: \"{user_input}\"
Devuelve SOLO el número de la opción (ejemplo: 4).
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Solo responde el número."},
                  {"role": "user", "content": prompt}],
        temperature=0
    )

    action = response.choices[0].message.content.strip()
    return action

def main():
    excel_file = os.path.join("data", "Proyectos CAPEX 2025.xlsx")
    manager = ProjectManager()
    manager.load_from_excel(excel_file)

    while True:
        print("\n===== ASISTENTE IA DE PLANIFICACIÓN (DEMO) =====")
        print("1 → Reporte general")
        print("2 → Consulta proyecto individual + Gantt")
        print("3 → Evaluar proyecto con IA")
        print("4 → Clasificación de riesgos")
        print("5 → Mostrar gráficas generales")
        print("\n🔎 Módulos IA")
        print("6 → Análisis riesgo predictivo IA")
        print("7 → Reporte ejecutivo IA")
        print("8 → Recomendaciones IA")
        print("9 → Análisis portafolio IA")
        print("10 → Benchmarking histórico")
        print("11 → Sugerir cronograma ideal")
        print("\n🤖 Agentes IA")
        print("12 → Monitoring Agent")
        print("13 → Alerting Agent")
        print("14 → Reporting Agent")
        print("15 → LAB IA (3 agentes juntos)")
        print("=================================================")
        print("Escribe 'salir' para terminar.\n")

        user_input = input("👤 Tú: ").strip()
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 Asistente finalizado. ¡Hasta luego!")
            break

        # ✅ Mejora: permite acción directa numérica o vía LLM
        if user_input.isdigit() and user_input in [str(i) for i in range(0, 16)]:
            action = user_input
        else:
            action = route_instruction_to_action(user_input)

        # Ejecutar acción
        if action == "1":
            report_general(manager)
        elif action == "2":
            consulta_proyecto(manager)
        elif action == "3":
            evaluar_proyecto(manager)
        elif action == "4":
            clasificar_riesgo(manager)
        elif action == "5":
            mostrar_graficas(manager)
        elif action == "6":
            predictive_risk_analysis(manager)
        elif action == "7":
            generate_executive_report(manager)
        elif action == "8":
            recommend_for_portfolio(manager)
        elif action == "9":
            portfolio_analysis(manager)
        elif action == "10":
            benchmarking_analysis(manager)
        elif action == "11":
            schedule_suggestion()
        elif action == "12":
            monitor_progress(manager.get_projects())
        elif action == "13":
            detect_alerts(manager.get_projects())
        elif action == "14":
            generate_simple_report(manager.get_projects())
        elif action == "15":
            print("\n===== IA MULTI-AGENT LAB =====")
            monitor_progress(manager.get_projects())
            detect_alerts(manager.get_projects())
            generate_simple_report(manager.get_projects())
        else:
            print("❌ No se pudo interpretar la instrucción. Intenta de nuevo.")

if __name__ == "__main__":
    main()
