# AIA
# Asistente IA para Planificación de Proyectos CAPEX

## 🎯 Descripción general
Proyecto académico + prototipo real de Asistente IA + Multi-Agente para planificación, seguimiento y análisis de portafolios de proyectos de construcción CAPEX.
Desarrollado en Python + IA Generativa + Data Science + Streamlit.

Autor: Arturo Santiago

El sistema permite:

- Analizar portafolios de proyectos
- Generar reportes y alertas automáticas
- Visualizar cronogramas y gráficas clave
- Clasificar riesgos automáticamente
- Sugerir cronogramas ideales
- Desplegar agentes especializados para seguimiento

Disponible en:

- Modo consola (`main_demo.py`)
- Modo aplicación web (`streamlit_demo.py`)

---

## 💻 Requisitos

- Python 3.9 o superior
- Clave API OpenAI (en `config.yaml`)
- Librerías Python (instalar abajo)

---

## 📥 Instalación

```bash
git clone https://github.com/asantiagodata9/AIA.git
cd AIA
python -m venv venv
venv\Scripts\activate   # En Windows
pip install -r requirements.txt
```


Crear archivo config.yaml:
```yaml
openai:
  api_key: TU_API_KEY_AQUI
```

Colocar dataset en:
```
data/Proyectos CAPEX 2025.xlsx
```

🚀 Cómo ejecutar
Modo consola:

```bash
python main_demo.py
```

Modo app web:

```bash
streamlit run streamlit_demo.py
```

🗂️ Estructura del proyecto
```swift
/data/
      Proyectos CAPEX 2025.xlsx
/planner/
      (módulos IA + Agentes)
/screenshots/
      (opcional: capturas para documentación)
main_demo.py
streamlit_demo.py
requirements.txt
README.md
config.yaml.example
.gitignore
```
---

🎛️ Descripción de módulos

## Sección 1:
Reporte general
Resumen proyectos: cantidad, monto total, días promedio.

Consulta individual
Despliega info + Gantt individual de cualquier proyecto.

Evaluar proyecto con IA
Asistente GPT analiza situación, riesgos, acciones.

Clasificación de riesgos
Clasifica riesgo (alto, medio, bajo) usando reglas.

Mostrar gráficas generales
Visualizaciones:

Cronograma global (Gantt)

Recursos asignados

Complejidad obras

## Sección 2:
Análisis riesgo predictivo (IA)
Predice probabilidad de riesgo en proyectos.

Reporte ejecutivo IA
Genera reporte resumen para Dirección.

Recomendaciones IA
Sugiere mejores prácticas para optimizar portafolio.

Análisis portafolio IA
Análisis global comportamiento proyectos.

Benchmarking histórico
Comparación desempeño vs. histórico.

Sugerir cronograma ideal
Genera propuesta fechas para nuevos proyectos.

🤖 Agentes IA Multi-Agent System
Monitoring Agent
Detecta proyectos estancados.

Alerting Agent (Mejorado)
Detecta hitos reales próximos o vencidos + recomienda acciones.

Reporting Agent
Resumen ejecutivo actual de portafolio.

LAB IA (3 agentes juntos)
Ejecuta secuencia completa multi-agente.

Screenshots (opcional)
Colocar imágenes en /screenshots/ y referenciar aquí:


Valor diferencial
Funcionalidad	Incluido
Data Science + pandas	✅
Visualizaciones matplotlib	✅
IA generativa OpenAI GPT	✅
Modo consola	✅
Modo web Streamlit	✅
Arquitectura multi-agente	✅
Proyecto realista y ampliable	✅

Créditos
Desarrollado por: Arturo Santiago
Asesorado por: ChatGPT (IA asistente)
Curso: Temas Selectos de Estadística / ITAM 2025
