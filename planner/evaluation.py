# planner/evaluation.py

from openai import OpenAI
from planner.models import Project
from planner.utils import load_config
import pandas as pd

def format_date(date_obj):
    if pd.isna(date_obj) or date_obj is None:
        return ""
    return pd.to_datetime(date_obj).strftime("%Y-%m-%d")

def print_project_summary(project: Project):
    print(f"""
===== INFORMACIÓN GENERAL DEL PROYECTO =====
ID RE: {project.id_re}
Marca: {project.marca}
Campus: {project.campus_conjunto}
Nombre Proyecto: {project.nombre_proyecto}
Año: {project.anio_capex_opex}
Categoría: {project.categoria_proyecto}
Monto autorizado: {project.monto_autorizado}
Proveedor de obra: {project.proveedor_obra}
Etapa actual: {project.etapa}
Complejidad: {project.complejidad_obra}

Fechas Planeadas y Reales:
- RU Planeado: {format_date(project.fecha_ru)} | RU Real: {format_date(project.fecha_ru_real)}
- ADC Planeado: {format_date(project.fecha_adc)} | ADC Real: {format_date(project.fecha_adc_real)}
- DB1/DB2 Planeado: {format_date(project.fecha_db1_db2)} | DB1/DB2 Real: {format_date(project.fecha_db1_db2_real)}
- Autorización DB1/DB2 Planeado: {format_date(project.fecha_autorizacion_db1_db2)} | Autorización DB1/DB2 Real: {format_date(project.fecha_autorizacion_db1_db2_real)}
- Licitación proveedor Planeado: {format_date(project.fecha_licitacion_proveedor)} | Real: {format_date(project.fecha_licitacion_proveedor_real)}
- Adjudicación Planeado: {format_date(project.fecha_adjudicacion)} | Real: {format_date(project.fecha_adjudicacion_real)}
- Contrato proceso Planeado: {format_date(project.fecha_contrato_proceso)} | Real: {format_date(project.fecha_contrato_proceso_real)}
- Contrato liberado Planeado: {format_date(project.fecha_contrato_liberado)} | Real: {format_date(project.fecha_contrato_liberado_real)}
- Inicio ejecución Planeado: {format_date(project.fecha_inicio)} | Real: {format_date(project.fecha_inicio_real)}
- Conclusión Planeado: {format_date(project.fecha_conclusion)} | Real: {format_date(project.fecha_conclusion_real)}
- Días programados: {project.dias_totales_programado}

Otros:
- Puntaje ADC: {project.puntaje_adc}
- ¿Requiere licencia?: {project.necesita_licencia}
============================================
""")

def format_project_for_gpt(project: Project) -> str:
    return f"""
EVALUACIÓN DE PROYECTO PARA ASISTENTE IA

ID RE: {project.id_re}
Marca: {project.marca}
Campus: {project.campus_conjunto}
Nombre Proyecto: {project.nombre_proyecto}
Año: {project.anio_capex_opex}
Categoría: {project.categoria_proyecto}
Monto autorizado: {project.monto_autorizado}
Proveedor de obra: {project.proveedor_obra}
Etapa actual: {project.etapa}
Complejidad: {project.complejidad_obra}

Fechas Planeadas y Reales:
- RU Planeado: {format_date(project.fecha_ru)} | RU Real: {format_date(project.fecha_ru_real)}
- ADC Planeado: {format_date(project.fecha_adc)} | ADC Real: {format_date(project.fecha_adc_real)}
- DB1/DB2 Planeado: {format_date(project.fecha_db1_db2)} | DB1/DB2 Real: {format_date(project.fecha_db1_db2_real)}
- Autorización DB1/DB2 Planeado: {format_date(project.fecha_autorizacion_db1_db2)} | Real: {format_date(project.fecha_autorizacion_db1_db2_real)}
- Licitación proveedor Planeado: {format_date(project.fecha_licitacion_proveedor)} | Real: {format_date(project.fecha_licitacion_proveedor_real)}
- Adjudicación Planeado: {format_date(project.fecha_adjudicacion)} | Real: {format_date(project.fecha_adjudicacion_real)}
- Contrato proceso Planeado: {format_date(project.fecha_contrato_proceso)} | Real: {format_date(project.fecha_contrato_proceso_real)}
- Contrato liberado Planeado: {format_date(project.fecha_contrato_liberado)} | Real: {format_date(project.fecha_contrato_liberado_real)}
- Inicio ejecución Planeado: {format_date(project.fecha_inicio)} | Real: {format_date(project.fecha_inicio_real)}
- Conclusión Planeado: {format_date(project.fecha_conclusion)} | Real: {format_date(project.fecha_conclusion_real)}
- Días programados: {project.dias_totales_programado}

Otros:
- Puntaje ADC: {project.puntaje_adc}
- ¿Requiere licencia?: {project.necesita_licencia}

Por favor, proporciona:
1️⃣ Un breve diagnóstico del estado general del proyecto.
2️⃣ Riesgos potenciales o alertas detectadas.
3️⃣ Recomendaciones prácticas para mejorar o acelerar su avance.
4️⃣ Desviaciones por etapa: presenta una tabla donde compares la fecha planeada y la fecha real para cada hito (RU firmado, ADC, DB1/DB2, adjudicación, contrato, inicio de ejecución, conclusión). 
    - Si alguna fecha real no está disponible, anota 'No disponible' en la tabla.
    - Si ambas fechas existen, calcula la diferencia en días:
        - Diferencia positiva = días de retraso (ejemplo: +30 días)
        - Diferencia cero = en tiempo
        - Diferencia negativa = días de adelanto (ejemplo: -15 días)
Entrega la respuesta en formato estructurado, con una tabla limpia y bien presentada.
"""

def evaluate_project_with_gpt(project: Project, model: str = "gpt-4o") -> str:
    print_project_summary(project)

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])

    prompt = format_project_for_gpt(project)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un experto en planificación y control de proyectos de construcción. Sé preciso, técnico y propositivo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content
