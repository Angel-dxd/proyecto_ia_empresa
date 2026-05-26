import json
import requests
import subprocess
import os

MODEL_BASE = "llama3"
MODEL_ENTRENADO = "asistente-maderas"
TRAINING_FILE = "training_data.json"

def ask_ollama(model, pregunta):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": pregunta, "stream": False},
        timeout=60
    )
    return r.json()["response"]

def cargar_training_data():
    with open(TRAINING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def crear_modelfile(datos):
    ejemplos = "\n".join(
        f"P: {d['pregunta']}\nR: {d['respuesta']}" for d in datos
    )
    modelfile = f"""FROM {MODEL_BASE}

SYSTEM \"\"\"
Eres el asistente virtual de una empresa de maderas y materiales de construccion.
Solo respondes sobre maderas, precios y caracteristicas de los materiales de nuestro catalogo.
Si te preguntan algo no relacionado con maderas, indica amablemente que solo puedes ayudar con ese tema.

Ejemplos de preguntas y respuestas de nuestro catalogo:
{ejemplos}
\"\"\"
"""
    return modelfile

def entrenar():
    datos = cargar_training_data()
    print(f"Cargados {len(datos)} pares pregunta-respuesta de entrenamiento.")

    modelfile_content = crear_modelfile(datos)
    modelfile_path = "Modelfile"

    with open(modelfile_path, "w", encoding="utf-8") as f:
        f.write(modelfile_content)
    print(f"Modelfile generado: {modelfile_path}")

    print(f"\nCreando modelo '{MODEL_ENTRENADO}' con Ollama...")
    result = subprocess.run(
        ["ollama", "create", MODEL_ENTRENADO, "-f", modelfile_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Modelo '{MODEL_ENTRENADO}' creado correctamente.")
    else:
        print(f"Error al crear el modelo: {result.stderr}")
        return False
    return True

def demo_antes_y_despues():
    preguntas_demo = [
        "¿Cuál es la madera más resistente?",
        "¿Qué madera recomendáis para exterior?",
        "¿Cuánto cuesta la Madera B?"
    ]

    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN: ANTES vs DESPUÉS del entrenamiento")
    print("=" * 60)

    for pregunta in preguntas_demo:
        print(f"\nPREGUNTA: {pregunta}")
        print("-" * 40)

        print(f"ANTES ({MODEL_BASE} genérico):")
        resp_antes = ask_ollama(MODEL_BASE, pregunta)
        print(f"  {resp_antes[:300]}...")

        print(f"\nDESPUÉS ({MODEL_ENTRENADO} entrenado):")
        resp_despues = ask_ollama(MODEL_ENTRENADO, pregunta)
        print(f"  {resp_despues[:300]}...")
        print()

if __name__ == "__main__":
    print("=== Entrenamiento de IA con pares Pregunta-Respuesta ===\n")
    print("1. Entrenar modelo (crear Modelfile y modelo Ollama)")
    print("2. Demo antes/después (sin reentrenar)")
    print("3. Entrenar Y mostrar demo")
    opcion = input("\nElige opción (1/2/3): ").strip()

    if opcion == "1":
        entrenar()
    elif opcion == "2":
        demo_antes_y_despues()
    elif opcion == "3":
        if entrenar():
            demo_antes_y_despues()
    else:
        print("Opción no válida.")
