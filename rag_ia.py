import requests
from rag_real import consultar, inicializar_db, DB_PATH
import os

MODEL = "llama3"

def ask_ollama(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    return r.json()["response"]

def rag_con_ia(pregunta, n_chunks=3):
    print(f"\nPregunta: {pregunta}")
    print("-" * 50)

    # Paso 1: recuperar chunks crudos del RAG
    resultados = consultar(pregunta, n_resultados=n_chunks)
    chunks_crudos = [chunk for chunk, _ in resultados]

    print("Chunks recuperados (datos crudos del RAG):")
    for i, chunk in enumerate(chunks_crudos, 1):
        print(f"  [{i}] {chunk[:100]}...")

    # Paso 2: pasar chunks a la IA para que genere respuesta humana
    contexto = "\n\n".join(chunks_crudos)
    prompt = f"""Eres un experto asesor de materiales de construcción.
Usa SOLO la información del contexto siguiente para responder la pregunta.
Responde en español, de forma clara y concisa para un usuario sin conocimientos técnicos.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:"""

    print("\nGenerando respuesta con IA...")
    respuesta = ask_ollama(prompt)
    return respuesta

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("Inicializando base de datos...")
        inicializar_db()

    print("=== RAG + IA: De chunks crudos a lenguaje humano ===\n")

    while True:
        pregunta = input("Tu pregunta (o 'salir'): ").strip()
        if pregunta.lower() == "salir":
            break
        if not pregunta:
            continue

        respuesta = rag_con_ia(pregunta)
        print(f"\nRespuesta IA:\n{respuesta}\n")
        print("=" * 60)
