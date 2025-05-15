# planner/models.py

import pandas as pd
from typing import List, Optional

class Project:
    def __init__(self,
                 id_re: str,
                 marca: str,
                 campus_conjunto: str,
                 nombre_proyecto: str,
                 anio_capex_opex: str,
                 categoria_proyecto: str,
                 monto_autorizado: float,
                 proveedor_obra: str,
                 etapa: str,
                 fecha_ru: Optional[pd.Timestamp],
                 fecha_ru_real: Optional[pd.Timestamp],
                 fecha_adc: Optional[pd.Timestamp],
                 fecha_adc_real: Optional[pd.Timestamp],
                 puntaje_adc: Optional[float],
                 necesita_licencia: Optional[str],
                 fecha_db1_db2: Optional[pd.Timestamp],
                 fecha_db1_db2_real: Optional[pd.Timestamp],
                 fecha_autorizacion_db1_db2: Optional[pd.Timestamp],
                 fecha_autorizacion_db1_db2_real: Optional[pd.Timestamp],
                 fecha_licitacion_proveedor: Optional[pd.Timestamp],
                 fecha_licitacion_proveedor_real: Optional[pd.Timestamp],
                 fecha_adjudicacion: Optional[pd.Timestamp],
                 fecha_adjudicacion_real: Optional[pd.Timestamp],
                 fecha_contrato_proceso: Optional[pd.Timestamp],
                 fecha_contrato_proceso_real: Optional[pd.Timestamp],
                 fecha_contrato_liberado: Optional[pd.Timestamp],
                 fecha_contrato_liberado_real: Optional[pd.Timestamp],
                 fecha_inicio: Optional[pd.Timestamp],
                 fecha_inicio_real: Optional[pd.Timestamp],
                 complejidad_obra: str,
                 fecha_conclusion: Optional[pd.Timestamp],
                 fecha_conclusion_real: Optional[pd.Timestamp],
                 dias_totales_programado: Optional[float]):

        self.id_re = id_re
        self.marca = marca
        self.campus_conjunto = campus_conjunto
        self.nombre_proyecto = nombre_proyecto
        self.anio_capex_opex = anio_capex_opex
        self.categoria_proyecto = categoria_proyecto
        self.monto_autorizado = monto_autorizado
        self.proveedor_obra = proveedor_obra
        self.etapa = etapa
        self.fecha_ru = fecha_ru
        self.fecha_ru_real = fecha_ru_real
        self.fecha_adc = fecha_adc
        self.fecha_adc_real = fecha_adc_real
        self.puntaje_adc = puntaje_adc
        self.necesita_licencia = necesita_licencia
        self.fecha_db1_db2 = fecha_db1_db2
        self.fecha_db1_db2_real = fecha_db1_db2_real
        self.fecha_autorizacion_db1_db2 = fecha_autorizacion_db1_db2
        self.fecha_autorizacion_db1_db2_real = fecha_autorizacion_db1_db2_real
        self.fecha_licitacion_proveedor = fecha_licitacion_proveedor
        self.fecha_licitacion_proveedor_real = fecha_licitacion_proveedor_real
        self.fecha_adjudicacion = fecha_adjudicacion
        self.fecha_adjudicacion_real = fecha_adjudicacion_real
        self.fecha_contrato_proceso = fecha_contrato_proceso
        self.fecha_contrato_proceso_real = fecha_contrato_proceso_real
        self.fecha_contrato_liberado = fecha_contrato_liberado
        self.fecha_contrato_liberado_real = fecha_contrato_liberado_real
        self.fecha_inicio = fecha_inicio
        self.fecha_inicio_real = fecha_inicio_real
        self.complejidad_obra = complejidad_obra
        self.fecha_conclusion = fecha_conclusion
        self.fecha_conclusion_real = fecha_conclusion_real
        self.dias_totales_programado = dias_totales_programado

class ProjectManager:

    COLUMNS = [
        "ID RE", "Marca", "Campus conjunto", "Nombre de Proyecto", "Año CAPEX/OPEX",
        "Categoría proyecto", "Obra Monto autorizado (administración)", "Proveedor de Obra", "Etapa",
        "02-Fecha de RU firmado (Kick off de seguimiento)", "02-Fecha de RU firmado (Kick off de seguimiento) Real",
        "04-ADC finalizado", "04-ADC finalizado Real",
        "Puntaje de ADC", "¿Necesita licencia de construcción?",
        "06-DB1/DB2 finalizado y enviado a firma", "06-DB1/DB2 finalizado y enviado a firma Real",
        "07-Autorización de DB1/DB2 del usuario", "07-Autorización de DB1/DB2 del usuario Real",
        "14-Licitación de Proveedor de obra en desarrollo", "14-Licitación de Proveedor de obra en desarrollo Real",
        "15-Confirmación de adjudicación", "15-Confirmación de adjudicación Real",
        "16-Contrato en proceso", "16-Contrato en proceso Real",
        "16.1-Contrato liberado", "16.1-Contrato liberado Real",
        "19-Inicio de ejecución", "19-Inicio de ejecución Real",
        "Complejidad de obra", "22-Conclusión de obra y entrega a usuario", "22-Conclusión de obra y entrega a usuario Real",
        "DÍAS TOTALES DEL PROYECTO (PROGRAMADO)"
    ]

    def __init__(self):
        self.projects: List[Project] = []

    def load_from_excel(self, file_path: str, sheet_name: str = "Proyectos 2025"):
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=self.COLUMNS)

        for _, row in df.iterrows():
            project = Project(
                id_re=row["ID RE"],
                marca=row["Marca"],
                campus_conjunto=row["Campus conjunto"],
                nombre_proyecto=row["Nombre de Proyecto"],
                anio_capex_opex=row["Año CAPEX/OPEX"],
                categoria_proyecto=row["Categoría proyecto"],
                monto_autorizado=row["Obra Monto autorizado (administración)"],
                proveedor_obra=row["Proveedor de Obra"],
                etapa=row["Etapa"],
                fecha_ru=row["02-Fecha de RU firmado (Kick off de seguimiento)"],
                fecha_ru_real=row["02-Fecha de RU firmado (Kick off de seguimiento) Real"],
                fecha_adc=row["04-ADC finalizado"],
                fecha_adc_real=row["04-ADC finalizado Real"],
                puntaje_adc=row["Puntaje de ADC"],
                necesita_licencia=row["¿Necesita licencia de construcción?"],
                fecha_db1_db2=row["06-DB1/DB2 finalizado y enviado a firma"],
                fecha_db1_db2_real=row["06-DB1/DB2 finalizado y enviado a firma Real"],
                fecha_autorizacion_db1_db2=row["07-Autorización de DB1/DB2 del usuario"],
                fecha_autorizacion_db1_db2_real=row["07-Autorización de DB1/DB2 del usuario Real"],
                fecha_licitacion_proveedor=row["14-Licitación de Proveedor de obra en desarrollo"],
                fecha_licitacion_proveedor_real=row["14-Licitación de Proveedor de obra en desarrollo Real"],
                fecha_adjudicacion=row["15-Confirmación de adjudicación"],
                fecha_adjudicacion_real=row["15-Confirmación de adjudicación Real"],
                fecha_contrato_proceso=row["16-Contrato en proceso"],
                fecha_contrato_proceso_real=row["16-Contrato en proceso Real"],
                fecha_contrato_liberado=row["16.1-Contrato liberado"],
                fecha_contrato_liberado_real=row["16.1-Contrato liberado Real"],
                fecha_inicio=row["19-Inicio de ejecución"],
                fecha_inicio_real=row["19-Inicio de ejecución Real"],
                complejidad_obra=row["Complejidad de obra"],
                fecha_conclusion=row["22-Conclusión de obra y entrega a usuario"],
                fecha_conclusion_real=row["22-Conclusión de obra y entrega a usuario Real"],
                dias_totales_programado=row["DÍAS TOTALES DEL PROYECTO (PROGRAMADO)"]
            )
            self.projects.append(project)

    def get_projects(self) -> List[Project]:
        return self.projects
