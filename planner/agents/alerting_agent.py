# alerting_agent.py

from planner.utils import load_config
from openai import OpenAI
from datetime import datetime
import pandas as pd

def detect_upcoming_alerts(project, days_threshold=7):
    print("\n===== ALERTING AGENT =====")
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
            fecha_dt = pd.to_datetime(fecha)  # asegura datetime
            days_remaining = (fecha_dt - today).days
            if days_remaining < 0:
                alerts.append(f"⚠️ {etapa} VENCIDA hace {abs(days_remaining)} días")
            elif days_remaining <= days_threshold:
                alerts.append(f"⚠️ {etapa} vence en {days_remaining} días")

    if not alerts:
        print("✅ No se detectaron fechas críticas.")
        return

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

    print("\n".join(alerts))
    print("\nRespuesta IA:\n")
    print(response.choices[0].message.content)
