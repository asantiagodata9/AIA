# planner/schedule_suggestion_ai.py

from planner.utils import load_config
from openai import OpenAI

def schedule_suggestion():
    print("\n===== GENERADOR DE CRONOGRAMA SUGERIDO =====")

    # Recoge datos básicos del usuario
    nombre = input("👉 Nombre del proyecto: ").strip()
    categoria = input("👉 Categoría del proyecto: ").strip()
    try:
        monto = float(input("👉 Monto estimado del proyecto: ").strip())
    except ValueError:
        monto = 0.0
    complejidad = input("👉 Complejidad esperada (baja / intermedia / compleja / extracompleja): ").strip()
    licencia = input("👉 ¿Requiere licencia? (sí / no): ").strip()

    prompt = f"""
Eres un experto planificador de proyectos de construcción.

Con base en los siguientes datos, sugiere un cronograma tentativo ideal para este nuevo proyecto:

- Nombre del proyecto: {nombre}
- Categoría: {categoria}
- Monto estimado: {monto}
- Complejidad: {complejidad}
- Requiere licencia: {licencia}

Incluye:
1. Las etapas recomendadas (kick off, DB1/DB2, autorizaciones, licitación, contratación, inicio obra, conclusión).
2. Una estimación en días desde el inicio para cada etapa.
3. Consejos adicionales para lograr una ejecución eficiente.

Entrega el resultado en formato tabla + recomendaciones adicionales.
"""

    config = load_config()
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asesor senior en planeación de obras."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result_text = response.choices[0].message.content
    print("\n===== CRONOGRAMA SUGERIDO =====")
    print(result_text)
