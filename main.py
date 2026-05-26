import requests
from rag import retrieve

MODEL = "llama3"

# --- OLLAMA ---
def ask_llm(prompt):
    print("  [IA generando respuesta, espera unos segundos...]")
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=90
        )
        if r.status_code != 200:
            return f"[Error Ollama: código {r.status_code}]"
        return r.json().get("response", "[Sin respuesta]")
    except requests.exceptions.Timeout:
        return "[Timeout: Ollama tardó demasiado. Intenta una pregunta más corta.]"
    except Exception as e:
        return f"[Error: {e}]"

# --- AGENTE ---
def agent(query):
    q = query.lower()

    # MCP (REGLAS INSTANTÁNEAS — sin llamar a Ollama)
    if "más caro" in q or "mas caro" in q:
        df = retrieve(query)
        row = df.loc[df["precio"].idxmax()]
        return f"[MCP] Material más caro: {row['nombre']} — Precio: {row['precio']}"

    if "más barato" in q or "mas barato" in q:
        df = retrieve(query)
        row = df.loc[df["precio"].idxmin()]
        return f"[MCP] Material más barato: {row['nombre']} — Precio: {row['precio']}"

    if "listar" in q or "todos" in q or "catálogo" in q or "catalogo" in q:
        df = retrieve(query)
        return f"[MCP] Catálogo completo:\n{df.to_string(index=False)}"

    # RAG (RECUPERACIÓN + IA)
    if "resistente" in q or "exterior" in q or "madera" in q or "recomienda" in q:
        df = retrieve(query)
        prompt = f"""Eres un asistente de materiales de construcción. Responde en español.

Datos del catálogo:
{df.to_string(index=False)}

Pregunta del cliente: {query}

Respuesta breve y directa:"""
        return ask_llm(prompt)

    # IA GENERAL (fallback)
    return ask_llm(query)


# --- LOOP PRINCIPAL ---
if __name__ == "__main__":
    print("Sistema IA empresarial activo (MCP + RAG + IA)")
    print("Modelo:", MODEL)
    print("Preguntas rápidas (MCP): 'más caro', 'más barato', 'listar todos'")
    print("Preguntas IA: cualquier cosa sobre maderas\n")

    while True:
        try:
            q = input("Pregunta: ").strip()
            if not q:
                continue
            respuesta = agent(q)
            print(f"Respuesta: {respuesta}\n")
        except KeyboardInterrupt:
            print("\nSaliendo del sistema...")
            break