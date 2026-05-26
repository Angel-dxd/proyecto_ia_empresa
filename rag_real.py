import chromadb
import os

CORPUS_FILE = "corpus.txt"
DB_PATH = "./chroma_db"

def cargar_chunks(filepath, chunk_size=200):
    with open(filepath, "r", encoding="utf-8") as f:
        texto = f.read()
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    return parrafos

def inicializar_db():
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection("materiales")
    except Exception:
        pass
    collection = client.create_collection(
        name="materiales",
        metadata={"hnsw:space": "cosine"}
    )

    chunks = cargar_chunks(CORPUS_FILE)
    print(f"Indexando {len(chunks)} chunks en ChromaDB...")

    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print("Base de datos vectorial lista.")
    return collection

def obtener_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection("materiales")

def consultar(query, n_resultados=3):
    collection = obtener_collection()
    resultados = collection.query(
        query_texts=[query],
        n_results=n_resultados
    )
    chunks = resultados["documents"][0]
    distancias = resultados["distances"][0]
    return list(zip(chunks, distancias))

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        inicializar_db()
    else:
        respuesta = input("¿Reinicializar base de datos? (s/n): ").strip().lower()
        if respuesta == "s":
            inicializar_db()

    print("\n=== RAG con ChromaDB ===")
    print("Escribe una pregunta sobre maderas (o 'salir' para terminar)\n")

    while True:
        query = input("Pregunta: ").strip()
        if query.lower() == "salir":
            break
        if not query:
            continue

        resultados = consultar(query)
        print(f"\nTop {len(resultados)} chunks más similares a: '{query}'\n")
        for i, (chunk, dist) in enumerate(resultados, 1):
            similitud = round((1 - dist) * 100, 1)
            print(f"[Chunk {i}] Similitud: {similitud}%")
            print(f"  {chunk[:200]}...")
            print()
