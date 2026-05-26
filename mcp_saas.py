"""
MCP MiniSaaS - Modelo Context Protocol

Flujo:
  1. Usuario hace pregunta en lenguaje humano
  2. IA transforma la pregunta a una petición estructurada (JSON)
  3. El SaaS procesa la petición y devuelve datos
  4. La IA interpreta los datos y responde en lenguaje humano
"""

import requests
import json
import pandas as pd

MODEL = "llama3"

# --- SaaS: API interna de datos ---
def saas_endpoint(accion, parametros=None):
    df = pd.read_csv("datos.csv")
    parametros = parametros or {}

    if accion == "listar":
        return df.to_dict(orient="records")

    elif accion == "buscar_por_nombre":
        nombre = parametros.get("nombre", "")
        resultado = df[df["nombre"].str.lower() == nombre.lower()]
        return resultado.to_dict(orient="records")

    elif accion == "filtrar_precio":
        max_precio = parametros.get("max_precio", 9999)
        resultado = df[df["precio"] <= max_precio]
        return resultado.to_dict(orient="records")

    elif accion == "filtrar_densidad":
        min_densidad = parametros.get("min_densidad", 0)
        resultado = df[df["densidad"] >= min_densidad]
        return resultado.to_dict(orient="records")

    elif accion == "mas_caro":
        fila = df.loc[df["precio"].idxmax()]
        return [fila.to_dict()]

    elif accion == "mas_barato":
        fila = df.loc[df["precio"].idxmin()]
        return [fila.to_dict()]

    else:
        return {"error": f"Acción desconocida: {accion}"}

# --- IA: Transformar pregunta humana en petición API ---
def ia_pregunta_a_peticion(pregunta_humana):
    prompt = f"""Eres un traductor de lenguaje natural a peticiones de API JSON.

API disponible con las siguientes acciones:
- listar: lista todos los materiales (sin parametros)
- buscar_por_nombre: {{nombre: "Madera A"}}
- filtrar_precio: {{max_precio: número}}
- filtrar_densidad: {{min_densidad: número decimal}}
- mas_caro: el material más caro (sin parametros)
- mas_barato: el material más barato (sin parametros)

Transforma esta pregunta del usuario en una petición JSON válida.
Responde SOLO con el JSON, sin explicaciones.

Pregunta: "{pregunta_humana}"

JSON:"""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )
    texto = r.json()["response"].strip()

    # Extraer JSON de la respuesta
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    if inicio >= 0 and fin > inicio:
        return json.loads(texto[inicio:fin])
    return None

# --- IA: Interpretar resultado del SaaS ---
def ia_interpretar_resultado(pregunta, datos):
    datos_str = json.dumps(datos, ensure_ascii=False, indent=2)
    prompt = f"""Eres un asistente de materiales de construcción.
El usuario preguntó: "{pregunta}"

La base de datos devolvió estos datos:
{datos_str}

Responde al usuario de forma clara, natural y en español.
Sé conciso y útil."""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    return r.json()["response"]

# --- FLUJO COMPLETO MCP ---
def mcp_consulta(pregunta_humana):
    print(f"\nUSUARIO: {pregunta_humana}")
    print("-" * 50)

    # Paso 1: IA transforma pregunta a petición API
    print("IA transformando pregunta a petición API...")
    peticion = ia_pregunta_a_peticion(pregunta_humana)
    if not peticion:
        print("Error: no se pudo generar la petición")
        return
    print(f"  → Petición generada: {json.dumps(peticion, ensure_ascii=False)}")

    # Paso 2: SaaS procesa la petición
    accion = peticion.get("accion", peticion.get("action", "listar"))
    parametros = {k: v for k, v in peticion.items() if k not in ("accion", "action")}
    datos = saas_endpoint(accion, parametros)
    print(f"  → SaaS respondió con {len(datos) if isinstance(datos, list) else 1} resultado(s)")

    # Paso 3: IA interpreta resultado para el usuario
    print("  → IA interpretando resultado...")
    respuesta_final = ia_interpretar_resultado(pregunta_humana, datos)
    print(f"\nRESPUESTA: {respuesta_final}")

if __name__ == "__main__":
    print("=== MCP MiniSaaS - Lenguaje Natural → API → Respuesta ===\n")
    print("Ejemplos de preguntas:")
    print("  - ¿Cuál es el material más barato?")
    print("  - Quiero materiales que no cuesten más de 15")
    print("  - ¿Cuánto cuesta la Madera B?")
    print("  - Busca materiales muy resistentes (densidad alta)\n")

    while True:
        pregunta = input("Tu pregunta (o 'salir'): ").strip()
        if pregunta.lower() == "salir":
            break
        if pregunta:
            mcp_consulta(pregunta)
            print()
