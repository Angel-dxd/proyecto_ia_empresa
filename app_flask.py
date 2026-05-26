from flask import Flask, render_template_string, request, jsonify
import chromadb
import requests
import os
import uuid

app = Flask(__name__)
DB_PATH = "./chroma_rag_flask"
MODEL = "llama3"

def get_or_create_collection(session_id):
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        return client.get_collection(session_id)
    except Exception:
        return client.create_collection(session_id)

def ask_ollama(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    return r.json()["response"]

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>RAG Empaquetado</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
    header { background: #1e293b; padding: 20px 40px; border-bottom: 1px solid #334155; }
    header h1 { color: #38bdf8; font-size: 1.6rem; }
    header p { color: #94a3b8; font-size: 0.9rem; margin-top: 4px; }
    .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
    h2 { color: #38bdf8; margin-bottom: 16px; font-size: 1.1rem; }
    textarea { width: 100%; padding: 12px; background: #0f172a; border: 1px solid #475569; border-radius: 8px;
               color: #e2e8f0; resize: vertical; font-size: 0.9rem; }
    input[type=text] { width: 100%; padding: 12px; background: #0f172a; border: 1px solid #475569;
                       border-radius: 8px; color: #e2e8f0; font-size: 0.9rem; }
    button { margin-top: 12px; padding: 10px 24px; background: #0284c7; border: none; border-radius: 8px;
             color: white; font-size: 0.95rem; cursor: pointer; transition: background 0.2s; }
    button:hover { background: #0369a1; }
    .result { margin-top: 16px; padding: 16px; background: #0f172a; border-radius: 8px;
              border-left: 3px solid #38bdf8; white-space: pre-wrap; font-size: 0.9rem; line-height: 1.6; display: none; }
    .chunk { background: #162032; border: 1px solid #334155; border-radius: 8px; padding: 12px;
             margin-bottom: 8px; font-size: 0.85rem; color: #94a3b8; }
    .badge { display: inline-block; padding: 2px 8px; background: #0c4a6e; color: #38bdf8;
             border-radius: 12px; font-size: 0.75rem; margin-bottom: 6px; }
    .status { color: #4ade80; font-size: 0.85rem; margin-top: 8px; }
    .error { color: #f87171; }
    .steps { display: flex; gap: 12px; margin-bottom: 20px; }
    .step { flex: 1; text-align: center; padding: 10px; background: #0f172a; border-radius: 8px; font-size: 0.8rem; }
    .step .num { font-size: 1.4rem; }
    .arrow { color: #475569; align-self: center; }
  </style>
</head>
<body>
  <header>
    <h1>RAG Empaquetado</h1>
    <p>Entrena tu propio sistema de búsqueda semántica con ChromaDB e IA</p>
  </header>
  <div class="container">

    <div class="steps">
      <div class="step"><div class="num">📄</div>1. Sube texto</div>
      <div class="arrow">→</div>
      <div class="step"><div class="num">🧠</div>2. ChromaDB indexa</div>
      <div class="arrow">→</div>
      <div class="step"><div class="num">🔍</div>3. Busca semánticamente</div>
      <div class="arrow">→</div>
      <div class="step"><div class="num">🤖</div>4. IA responde</div>
    </div>

    <div class="card">
      <h2>Paso 1 — Entrenar el RAG con tu texto</h2>
      <textarea id="trainText" rows="8" placeholder="Pega aquí el texto que quieres que la IA aprenda...&#10;&#10;Ejemplo: documentación, artículos, manuales, etc."></textarea>
      <button onclick="entrenar()">Entrenar RAG</button>
      <div id="trainStatus" class="status"></div>
    </div>

    <div class="card">
      <h2>Paso 2 — Consultar el RAG</h2>
      <input type="text" id="queryInput" placeholder="Escribe tu pregunta..." onkeydown="if(event.key==='Enter') consultar()"/>
      <button onclick="consultar()">Buscar</button>

      <div id="chunksResult" class="result"></div>
      <div id="iaResult" class="result"></div>
    </div>
  </div>

  <script>
    const SESSION = '{{ session_id }}';

    async function entrenar() {
      const texto = document.getElementById('trainText').value.trim();
      if (!texto) return alert('Escribe algún texto primero.');
      document.getElementById('trainStatus').textContent = 'Entrenando...';

      const res = await fetch('/train', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({texto, session: SESSION})
      });
      const data = await res.json();
      document.getElementById('trainStatus').textContent =
        data.ok ? `✓ ${data.chunks} chunks indexados en ChromaDB` : '✗ Error: ' + data.error;
    }

    async function consultar() {
      const query = document.getElementById('queryInput').value.trim();
      if (!query) return;

      document.getElementById('chunksResult').style.display = 'block';
      document.getElementById('chunksResult').textContent = 'Buscando chunks similares...';
      document.getElementById('iaResult').style.display = 'none';

      const res = await fetch('/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query, session: SESSION})
      });
      const data = await res.json();
      if (!data.ok) {
        document.getElementById('chunksResult').textContent = '✗ Error: ' + data.error;
        return;
      }

      let chunksHtml = '<b>Chunks más similares (datos crudos del RAG):</b><br><br>';
      data.chunks.forEach((c, i) => {
        chunksHtml += `<div class="chunk"><span class="badge">Chunk ${i+1} · ${c.similitud}% similitud</span><br>${c.texto}</div>`;
      });
      document.getElementById('chunksResult').innerHTML = chunksHtml;

      document.getElementById('iaResult').style.display = 'block';
      document.getElementById('iaResult').textContent = 'IA generando respuesta...';

      const res2 = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query, chunks: data.chunks.map(c => c.texto)})
      });
      const data2 = await res2.json();
      document.getElementById('iaResult').innerHTML = '<b>Respuesta de la IA:</b><br><br>' + data2.respuesta;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    session_id = "rag_" + str(uuid.uuid4())[:8]
    return render_template_string(HTML, session_id=session_id)

@app.route("/train", methods=["POST"])
def train():
    try:
        data = request.json
        texto = data.get("texto", "")
        session_id = data.get("session", "default")

        parrafos = [p.strip() for p in texto.split("\n\n") if len(p.strip()) > 30]
        if not parrafos:
            parrafos = [texto[i:i+300] for i in range(0, len(texto), 300) if texto[i:i+300].strip()]

        collection = get_or_create_collection(session_id)
        collection.add(
            documents=parrafos,
            ids=[f"{session_id}_{i}" for i in range(len(parrafos))]
        )
        return jsonify({"ok": True, "chunks": len(parrafos)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/query", methods=["POST"])
def query():
    try:
        data = request.json
        query_text = data.get("query", "")
        session_id = data.get("session", "default")

        collection = get_or_create_collection(session_id)
        results = collection.query(query_texts=[query_text], n_results=3)

        chunks = []
        for doc, dist in zip(results["documents"][0], results["distances"][0]):
            chunks.append({
                "texto": doc,
                "similitud": round((1 - dist) * 100, 1)
            })
        return jsonify({"ok": True, "chunks": chunks})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        query_text = data.get("query", "")
        chunks = data.get("chunks", [])

        contexto = "\n\n".join(chunks)
        prompt = f"""Responde la siguiente pregunta usando SOLO el contexto proporcionado.
Responde en español, de forma clara y útil.

CONTEXTO:
{contexto}

PREGUNTA: {query_text}

RESPUESTA:"""

        respuesta = ask_ollama(prompt)
        return jsonify({"ok": True, "respuesta": respuesta})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    print("RAG Empaquetado iniciando en http://localhost:5000")
    app.run(debug=True, port=5000)
