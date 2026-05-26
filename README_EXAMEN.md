# Guía de Examen — SSGG y Procesos
**Angel Xavier** | Mayo 2026

---

## Arrancar siempre primero

**Terminal 1 — Ollama (déjala abierta siempre):**
```bash
ollama serve
```

**Terminal 2 — Tu proyecto:**
```bash
cd /Users/angelxavier/proyecto_ia_empresa
source venv/bin/activate
```

---

# SISTEMAS DE GESTIÓN EMPRESARIAL (SSGG)

---

## 1. Ollama + Modelos
**Archivo:** `main.py` | **Comando:** `python main.py`

### Guion del vídeo (en orden):
1. Abre una terminal y ejecuta `ollama list` — muestra que tienes `llama3` instalado
2. Ejecuta `python main.py`
3. Escribe: `¿Cuál es el material más caro?` → espera la respuesta
4. Escribe: `¿Qué madera recomiendas para muebles de exterior?` → espera la respuesta
5. (Opcional) Abre el Monitor de Actividad de Mac mientras responde para mostrar el uso de RAM/CPU

### Si Vicente pregunta por qué elegiste llama3:
> "Usamos LLaMA 3 de Meta AI porque pesa 4.7 GB, responde en menos de 5 segundos en local, entiende bien el español y no requiere pagar por API. Lo comparamos con Mistral (menos preciso en español) y con GPT-4 (de pago y externo). LLaMA 3 local es el mejor equilibrio entre potencia, privacidad y coste cero."

---

## 2. Entrenamiento de IA
**Archivos:** `entrenamiento.py` + `training_data.json` | **Comando:** `python entrenamiento.py`

### Guion del vídeo (en orden):
1. Muestra el archivo `training_data.json` abierto en el editor (los pares pregunta-respuesta)
2. Ejecuta el programa, elige opción **1** (solo entrenar)
3. Mientras entrena (~1 min), explica verbalmente o con texto lo que está pasando
4. Cuando termine, elige opción **2** (demo antes/después)
5. La pantalla muestra la **MISMA pregunta** respondida por llama3 genérico vs asistente-maderas entrenado
6. El contraste tiene que verse claramente — ese es el núcleo del vídeo

### Lo que tiene que quedar claro en el vídeo:
- El JSON con pares pregunta-respuesta (los "datos de entrenamiento")
- La respuesta genérica del modelo base
- La respuesta específica del modelo entrenado

---

## 3. MCP — MiniSaaS ⭐ MUY IMPORTANTE
**Archivo:** `mcp_saas.py` | **Comando:** `python mcp_saas.py`

### Guion del vídeo (en orden):
1. Escribe: `¿Cuánto cuesta la Madera B?`
2. El programa muestra los **3 pasos en pantalla**:
   - Petición JSON generada por la IA (la transformación)
   - Datos crudos del SaaS
   - Respuesta interpretada en lenguaje humano
3. Escribe: `Quiero materiales que no cuesten más de 15`
4. Muestra de nuevo los 3 pasos
5. Escribe: `busca la madera más resistente`

### Lo que tiene que quedar claro:
El flujo completo paso a paso — pregunta humana → JSON/API → datos crudos → respuesta humana

---

## 4. IA Agéntica
**Archivo:** `agente_autonomo.py` | **Comando:** `python agente_autonomo.py`

### Guion del vídeo (en orden):
1. Elige misión **2** ("Encuentra el material más rentable")
2. Una vez elegida la misión, **no toques nada más** — el agente trabaja solo
3. Graba en pantalla cómo aparecen los pasos automáticamente: qué herramienta elige, qué resultado obtiene, qué decide hacer a continuación
4. Al final aparece el informe completo generado de forma autónoma
5. Señala verbalmente (o con texto en el vídeo) que no has intervenido en ningún momento

### Lo que tiene que quedar claro:
No parece un chatbot — parece un agente tomando decisiones y trabajando solo.

---

# PROGRAMACIÓN DE SERVICIOS Y PROCESOS

---

## 5. RAG con ChromaDB
**Archivo:** `rag_real.py` | **Comando:** `python rag_real.py`

### Guion del vídeo (en orden):
1. Muestra el archivo `corpus.txt` abierto (el texto largo de entrada)
2. Si la BD no existe, ejecuta y muestra cómo indexa los **8 chunks**
3. Si ya existe, responde **s** para reinicializar y mostrar el proceso desde cero
4. Escribe: `madera resistente al agua exterior` → muestra chunks con % similitud
5. Escribe: `construccion naval barcos` → muestra que encuentra teca aunque no diga "barcos" en el corpus
6. Destaca verbalmente: "la palabra 'barcos' no está en el texto, pero el sistema entiende el significado"

### Lo que tiene que quedar claro:
- El texto de entrada → se divide en chunks → ChromaDB los indexa → la query devuelve los más similares semánticamente (no los primeros)

---

## 6. RAG + IA
**Archivo:** `rag_ia.py` | **Comando:** `python rag_ia.py`

### Guion del vídeo (en orden):
1. Escribe: `qué madera uso para una terraza exterior`
2. El programa muestra primero los **chunks crudos** (texto feo, fragmentos técnicos)
3. Luego la **respuesta de la IA** (texto limpio, lenguaje humano)
4. Escribe: `cuál es la madera más económica para interiores`
5. Muestra de nuevo chunks crudos vs respuesta IA
6. Señala en pantalla la diferencia visual entre los dos bloques

### Lo que tiene que quedar claro:
El "antes" (chunks crudos, ilegible para un usuario) vs el "después" (respuesta humanizada) — ese contraste es el núcleo del vídeo.

---

## 7. RAG Empaquetado (Flask)
**Archivo:** `app_flask.py` | **Comando:** `python app_flask.py` → abrir `http://localhost:5000`

### Guion del vídeo (en orden):
1. Muestra la interfaz web completa en el navegador
2. **Como si fueras un usuario cualquiera**, pega este texto en el cuadro y pulsa "Entrenar RAG":
```
La madera de roble es muy resistente, ideal para suelos y carpintería de calidad.

El pino es la madera más económica. Se usa en muebles básicos y marcos de ventanas.

La teca resiste el agua y los insectos de forma natural. Perfecta para terrazas y jardines.

El cedro tiene aroma natural que repele insectos. Se usa en armarios y revestimientos.
```
3. Muestra el mensaje "X chunks indexados en ChromaDB"
4. Escribe en el buscador: `madera para jardín` → muestra chunks + respuesta IA
5. Escribe: `qué madera es más barata` → muestra resultado

### Lo que tiene que quedar claro:
Todo desde la interfaz web, sin tocar código. Cualquier usuario puede entrenar su propio RAG.

---

## 8. CSS 3D
**Archivo:** `css3d.html` | **Comando:** `open css3d.html`

### Guion del vídeo (en orden):
1. Muestra la escena 3D completa — el cubo rotando, los chunks flotando, las partículas
2. Pasa el ratón por encima del cubo para pausar la rotación
3. Pasa el ratón por los chunks de la izquierda para mostrar los efectos hover
4. Baja al buscador interactivo y escribe: `madera para lluvia`
5. Muestra cómo aparecen los chunks con porcentaje de similitud y la respuesta de la IA
6. Escribe: `instrumento musical`
7. Señala los efectos de perspectiva 3D, rotaciones y transiciones

### Lo que tiene que quedar claro:
Va más allá de CSS básico — hay un entorno 3D real con interactividad y RAG integrado.

---

# Checklist antes de grabar cada vídeo

- [ ] La app arranca sin errores visibles
- [ ] Zoom de pantalla al 125-150% para que el texto sea legible
- [ ] Se ve el flujo completo de inicio a resultado
- [ ] Dura entre 1 y 3 minutos
- [ ] Para entrenamiento: el antes/después está claro en pantalla
- [ ] Para RAG: se ven los chunks crudos y la respuesta final por separado

---

# Checklist final (antes del examen)

- [ ] `ollama serve` corriendo
- [ ] `source venv/bin/activate`
- [ ] `python rag_real.py` — funciona ✅
- [ ] `python rag_ia.py` — funciona ✅
- [ ] `python app_flask.py` + localhost:5000 — funciona ✅
- [ ] `python mcp_saas.py` — funciona ✅
- [ ] `python agente_autonomo.py` — funciona ✅
- [ ] `python entrenamiento.py` — funciona ✅
- [ ] `python main.py` — funciona ✅
- [ ] `open css3d.html` — funciona ✅
- [ ] 8 vídeos grabados (1-3 min cada uno)
- [ ] Textos de `textos_examen.md` copiados a Google Docs
- [ ] Google Doc compartido con Vicente

---

# Si algo falla

**Ollama no responde:**
```bash
ollama serve
```

**Error de módulo no encontrado:**
```bash
source venv/bin/activate
pip install chromadb flask
```

**ChromaDB da error:**
```bash
rm -rf chroma_db chroma_rag_flask
python rag_real.py
```

**Modelo entrenado no existe:**
```bash
python entrenamiento.py   # elige opción 1
```
