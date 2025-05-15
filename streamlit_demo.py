# streamlit_demo.py

import streamlit as st
import sys

# StreamlitLogger para redirigir print() a Streamlit
class StreamlitLogger:
    def write(self, message):
        if message.strip() != "":
            st.text(message)
    def flush(self):
        pass

sys.stdout = StreamlitLogger()

import pandas as pd
from planner.models import ProjectManager
from planner.visualizations import (
    plot_gantt,
    plot_resources,
    plot_complexity,
    plot_gantt_individual
)
from planner.evaluation import evaluate_project_with_gpt
from planner.risk_analysis import classify_all_projects
from planner.predictive_risk_ai import predictive_risk_analysis
from planner.executive_report_ai import generate_executive_report
from planner.recommendations_ai import recommend_for_portfolio
from planner.portfolio_analysis_ai import portfolio_analysis
from planner.benchmarking_ai import benchmarking_analysis
from planner.schedule_suggestion_ai import schedule_suggestion
from planner.agents.monitoring_agent import monitor_progress
from planner.agents.reporting_agent import generate_simple_report
from planner.utils import load_config
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="Asistente IA Proyectos", layout="wide")
st.title("📊 Asistente IA para Planificación de Proyectos CAPEX")

# Cargar datos
manager = ProjectManager()
manager.load_from_excel("data/Proyectos CAPEX 2025.xlsx")
projects = manager.get_projects()

menu = st.sidebar.selectbox("Selecciona una opción", [
    "Reporte general",
    "Consulta individual de proyecto",
    "Evaluar proyecto con IA",
    "Clasificación de riesgos",
    "Mostrar gráficas generales",
    "Análisis riesgo predictivo (IA)",
    "Reporte ejecutivo IA",
    "Recomendaciones IA",
    "Análisis portafolio IA",
    "Benchmarking histórico",
    "Sugerir cronograma ideal",
    "---",
    "Monitoring Agent",
    "Alerting Agent",
    "Reporting Agent",
    "LAB IA (3 agentes juntos)"
])

if menu == "Reporte general":
    st.header("📋 Reporte general del portafolio")
    total = len(projects)
    monto = sum([p.monto_autorizado for p in projects if pd.notna(p.monto_autorizado)])
    dias = [p.dias_totales_programado for p in projects if pd.notna(p.dias_totales_programado)]
    st.metric("Total proyectos", total)
    st.metric("Monto total autorizado", f"${monto:,.2f}")
    if dias:
        st.metric("Días promedio programados", f"{pd.Series(dias).mean():.2f}")

elif menu == "Consulta individual de proyecto":
    st.header("🔎 Consulta de proyecto")
    ids = [p.id_re for p in projects]
    selected = st.selectbox("Selecciona ID RE del proyecto", ids)
    project = next(p for p in projects if p.id_re == selected)
    st.subheader(f"Proyecto: {project.nombre_proyecto}")
    st.text(f"Campus: {project.campus_conjunto}\nEtapa: {project.etapa}\nMonto: {project.monto_autorizado}")
    fig = plot_gantt_individual(project)
    st.pyplot(fig)

elif menu == "Evaluar proyecto con IA":
    st.header("🤖 Evaluación IA del proyecto")
    ids = [p.id_re for p in projects]
    selected = st.selectbox("Selecciona ID RE del proyecto", ids)
    project = next(p for p in projects if p.id_re == selected)
    result = evaluate_project_with_gpt(project)
    st.text(result)

elif menu == "Clasificación de riesgos":
    st.header("🚦 Clasificación de riesgos")
    results = classify_all_projects(projects)
    df = pd.DataFrame(results, columns=["ID RE", "Proyecto", "Riesgo"])
    st.dataframe(df)

elif menu == "Mostrar gráficas generales":
    st.header("📊 Gráficas del portafolio")
    col1, col2 = st.columns(2)
    with col1:
        fig = plot_gantt(projects)
        st.pyplot(fig)
    with col2:
        fig = plot_resources(projects)
        st.pyplot(fig)
    fig = plot_complexity(projects)
    st.pyplot(fig)

elif menu == "Análisis riesgo predictivo (IA)":
    st.header("📉 Análisis riesgo predictivo IA")
    predictive_risk_analysis(manager)

elif menu == "Reporte ejecutivo IA":
    st.header("📋 Reporte ejecutivo IA")
    generate_executive_report(manager)

elif menu == "Recomendaciones IA":
    st.header("💡 Recomendaciones de mejores prácticas IA")
    recommend_for_portfolio(manager)

elif menu == "Análisis portafolio IA":
    st.header("📊 Análisis estratégico de portafolio IA")
    portfolio_analysis(manager)

elif menu == "Benchmarking histórico":
    st.header("📈 Benchmarking histórico del portafolio")
    benchmarking_analysis(manager)

elif menu == "Sugerir cronograma ideal":
    st.header("🗓️ Generador de cronograma sugerido")
    schedule_suggestion()

elif menu == "Monitoring Agent":
    st.header("👷 Monitoring Agent")
    monitor_progress(manager.get_projects())

elif menu == "Alerting Agent":
    st.header("🚨 Alerting Agent")
    ids = [p.id_re for p in projects]
    selected = st.selectbox("Selecciona ID RE del proyecto", ids)
    project = next(p for p in projects if p.id_re == selected)
    days = st.slider("Define umbral de días para alertas próximas", min_value=1, max_value=30, value=7)
    st.info(f"Alertas se activarán si alguna fecha real vence en los próximos {days} días.")

    # NUEVO Alerting Agent usando fechas reales
    fechas = {
        "RU firmado": project.fecha_ru_real,
        "ADC finalizado": project.fecha_adc_real,
        "DB1/DB2": project.fecha_db1_db2_real,
        "Autorización DB1/DB2": project.fecha_autorizacion_db1_db2_real,
        "Licitación proveedor": project.fecha_licitacion_proveedor_real,
        "Adjudicación": project.fecha_adjudicacion_real,
        "Contrato en proceso": project.fecha_contrato_proceso_real,
        "Contrato liberado": project.fecha_contrato_liberado_real,
        "Inicio ejecución": project.fecha_inicio_real,
        "Conclusión real": project.fecha_conclusion_real
    }

    alerts = []
    today = datetime.today()

    for etapa, fecha in fechas.items():
        if fecha is not None and pd.notna(fecha):
            fecha_dt = pd.to_datetime(fecha)
            days_remaining = (fecha_dt - today).days
            if days_remaining < 0:
                alerts.append(f"⚠️ {etapa} VENCIDA hace {abs(days_remaining)} días")
            elif days_remaining <= days:
                alerts.append(f"⚠️ {etapa} vence en {days_remaining} días")

    if alerts:
        st.warning("\n".join(alerts))
        alerts_text = "\n".join(alerts)
        prompt = f"""
Eres un agente de alertas. Este es el estado del proyecto "{project.nombre_proyecto}":
{alerts_text}
Sugiere acciones inmediatas para mitigar el riesgo de vencimiento.
"""
        config = load_config()
        client = OpenAI(api_key=config["openai"]["api_key"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Eres un agente de alertas proactivo."},
                      {"role": "user", "content": prompt}],
            temperature=0.2
        )
        st.subheader("Recomendaciones IA:")
        st.text(response.choices[0].message.content)
    else:
        st.success("✅ No se detectaron fechas críticas.")

elif menu == "Reporting Agent":
    st.header("📝 Reporting Agent")
    generate_simple_report(manager.get_projects())

elif menu == "LAB IA (3 agentes juntos)":
    st.header("🤖 IA MULTI-AGENT LAB")
    monitor_progress(manager.get_projects())
    from planner.agents.alerting_agent import detect_upcoming_alerts
    ids = [p.id_re for p in projects]
    detect_upcoming_alerts(next(p for p in projects if p.id_re == ids[0]))
    generate_simple_report(manager.get_projects())
