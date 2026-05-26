import requests
import json
import pandas as pd

MODEL = "llama3"

def ask_ollama(prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    r = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": MODEL, "messages": messages, "stream": False},
        timeout=60
    )
    return r.json()["message"]["content"]

# --- HERRAMIENTAS DISPONIBLES PARA EL AGENTE ---

def herramienta_listar_materiales():
    df = pd.read_csv("datos.csv")
    return df.to_string(index=False)

def herramienta_material_mas_caro():
    df = pd.read_csv("datos.csv")
    fila = df.loc[df["precio"].idxmax()]
    return f"{fila['nombre']} - Precio: {fila['precio']} - Densidad: {fila['densidad']}"

def herramienta_material_mas_barato():
    df = pd.read_csv("datos.csv")
    fila = df.loc[df["precio"].idxmin()]
    return f"{fila['nombre']} - Precio: {fila['precio']} - Densidad: {fila['densidad']}"

def herramienta_material_mas_resistente():
    df = pd.read_csv("datos.csv")
    fila = df.loc[df["densidad"].idxmax()]
    return f"{fila['nombre']} - Densidad: {fila['densidad']} - Precio: {fila['precio']}"

def herramienta_calcular_relacion_calidad_precio():
    df = pd.read_csv("datos.csv")
    df["calidad_precio"] = df["densidad"] / df["precio"]
    mejor = df.loc[df["calidad_precio"].idxmax()]
    return (
        f"Mejor relación calidad/precio: {mejor['nombre']}\n"
        f"  Precio: {mejor['precio']} | Densidad: {mejor['densidad']} | "
        f"Ratio: {mejor['calidad_precio']:.4f}"
    )

HERRAMIENTAS = {
    "listar_materiales": herramienta_listar_materiales,
    "material_mas_caro": herramienta_material_mas_caro,
    "material_mas_barato": herramienta_material_mas_barato,
    "material_mas_resistente": herramienta_material_mas_resistente,
    "calcular_relacion_calidad_precio": herramienta_calcular_relacion_calidad_precio,
}

SYSTEM_AGENTE = """Eres un agente de IA autónomo especializado en análisis de materiales de construcción.
Tu misión es completar tareas de análisis de forma AUTÓNOMA, usando las herramientas disponibles.

Herramientas disponibles (responde con el nombre exacto entre corchetes):
- [listar_materiales]: Lista todos los materiales del catálogo
- [material_mas_caro]: Obtiene el material más caro
- [material_mas_barato]: Obtiene el material más barato
- [material_mas_resistente]: Obtiene el material con mayor densidad
- [calcular_relacion_calidad_precio]: Calcula qué material tiene mejor relación calidad/precio

Para cada paso:
1. Decide qué herramienta usar y escribe [nombre_herramienta]
2. Cuando tengas toda la información, escribe [FINALIZAR] seguido de tu informe final.

Responde SOLO con una acción por vez."""

def ejecutar_agente(mision):
    print(f"\nMISIÓN: {mision}")
    print("=" * 60)
    print("Agente iniciando análisis autónomo...\n")

    historial = []
    pasos_max = 6
    paso = 0

    prompt_inicial = f"Misión asignada: {mision}\n\nComienza tu análisis. ¿Qué herramienta usas primero?"

    respuesta = ask_ollama(prompt_inicial, system=SYSTEM_AGENTE)
    historial.append(f"AGENTE: {respuesta}")

    while paso < pasos_max:
        paso += 1
        print(f"[Paso {paso}] {respuesta[:200]}")

        if "[FINALIZAR]" in respuesta:
            informe = respuesta.split("[FINALIZAR]", 1)[-1].strip()
            print("\n" + "=" * 60)
            print("INFORME FINAL DEL AGENTE:")
            print("=" * 60)
            print(informe)
            return

        # Detectar qué herramienta quiere usar
        herramienta_usada = None
        for nombre in HERRAMIENTAS:
            if f"[{nombre}]" in respuesta:
                herramienta_usada = nombre
                break

        if herramienta_usada:
            resultado = HERRAMIENTAS[herramienta_usada]()
            print(f"  → Ejecutando '{herramienta_usada}'...")
            print(f"  → Resultado: {resultado[:150]}...")

            contexto = "\n".join(historial[-4:])
            prompt_siguiente = (
                f"{contexto}\n\n"
                f"Resultado de [{herramienta_usada}]:\n{resultado}\n\n"
                f"¿Qué herramienta usas ahora, o ya tienes suficiente información para finalizar con [FINALIZAR]?"
            )
        else:
            prompt_siguiente = (
                f"Respuesta anterior: {respuesta}\n\n"
                f"Indica qué herramienta usar ([nombre_herramienta]) o finaliza con [FINALIZAR]."
            )

        respuesta = ask_ollama(prompt_siguiente, system=SYSTEM_AGENTE)
        historial.append(f"AGENTE: {respuesta}")

    print("\n[Agente alcanzó el límite de pasos]")

if __name__ == "__main__":
    print("=== Agente Autónomo de Análisis de Materiales ===")
    print("\nMisiones disponibles:")
    print("  1. Analizar el catálogo completo y recomendar el mejor material")
    print("  2. Encontrar el material más rentable para construcción")
    print("  3. Hacer un informe comparativo de todos los materiales")
    print("  4. Misión personalizada")

    opcion = input("\nElige (1/2/3/4): ").strip()
    misiones = {
        "1": "Analiza todo el catálogo de materiales y haz una recomendación final justificada.",
        "2": "Encuentra el material más rentable en términos de resistencia por unidad de coste.",
        "3": "Elabora un informe comparativo completo de todos los materiales disponibles.",
    }

    if opcion in misiones:
        ejecutar_agente(misiones[opcion])
    elif opcion == "4":
        mision = input("Describe tu misión: ").strip()
        ejecutar_agente(mision)
    else:
        print("Opción no válida.")
