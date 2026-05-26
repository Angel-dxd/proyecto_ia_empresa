# Textos del Examen — SSGG y Procesos
## Formato: 1 intro + 2 uso + 2 tecnologías + 1 cierre

---

## SISTEMAS DE GESTIÓN EMPRESARIAL (SSGG)

---

### 1. Ollama + Modelos de IA

**Introducción**
Este proyecto consiste en el desarrollo de un sistema de consulta inteligente que utiliza modelos de inteligencia artificial ejecutados de forma local mediante la herramienta Ollama. El objetivo principal es permitir a una empresa de materiales de construcción disponer de un asistente conversacional que responda preguntas sobre su catálogo sin depender de servicios externos ni internet, garantizando así la privacidad de los datos y reduciendo los costes operativos.

**Uso del programa (1)**
Para utilizar el sistema, el usuario inicia el programa ejecutando `python main.py` desde la terminal. El sistema muestra un prompt interactivo donde el usuario puede escribir cualquier pregunta en lenguaje natural, como "¿Cuál es el material más resistente?" o "¿Qué madera recomendáis para un mueble de exterior?". El programa envía la consulta al modelo de IA local y devuelve una respuesta en pocos segundos, sin conexión a internet.

**Uso del programa (2)**
El sistema está diseñado para integrarse en el flujo de trabajo diario de la empresa. Los empleados pueden consultarlo desde cualquier terminal de la red local sin necesidad de crear cuentas ni configurar APIs externas. Si el usuario interrumpe el programa con Ctrl+C, el sistema se cierra de forma limpia mostrando un mensaje de despedida. La interfaz es minimalista y eficiente, pensada para usuarios con conocimientos básicos de informática.

**Tecnologías (1)**
El núcleo del sistema es **Ollama**, una herramienta de código abierto que permite ejecutar modelos de lenguaje grande (LLM) de forma local. El modelo elegido ha sido **LLaMA 3** (Meta AI), seleccionado por su equilibrio entre potencia y consumo de recursos: ofrece respuestas de alta calidad con tan solo 4-8 GB de VRAM, lo que lo hace viable en hardware de empresa estándar. La comunicación con Ollama se realiza a través de su API REST local en `localhost:11434`.

**Tecnologías (2)**
El programa está desarrollado en **Python 3**, utilizando la librería `requests` para realizar peticiones HTTP a la API de Ollama. El modelo recibe el prompt del usuario y devuelve la respuesta en formato JSON, que el programa extrae y muestra al usuario. Se ha optado por LLaMA 3 frente a alternativas como Mistral o Phi-3 porque ofrece mejor comprensión del español y mayor capacidad de razonamiento sobre datos estructurados, con un consumo de memoria moderado (8B parámetros).

**Cierre**
Con este proyecto he aprendido cómo funcionan los modelos de lenguaje locales, cómo se comunican mediante APIs REST y qué parámetros influyen en la calidad y velocidad de las respuestas. También he comprendido la importancia de elegir el modelo adecuado según los recursos disponibles. Como mejora futura, implementaría una interfaz gráfica web en lugar de la terminal, y añadiría la posibilidad de cambiar de modelo en tiempo de ejecución para comparar respuestas de distintos LLMs sin modificar el código.

---

### 2. Entrenamiento de IA

**Introducción**
Este proyecto aborda el proceso de personalización de un modelo de inteligencia artificial mediante técnicas de entrenamiento orientado al dominio. A través de pares de preguntas y respuestas almacenados en formato JSON, se adapta el comportamiento de un modelo base genérico para que responda de forma específica y precisa sobre el catálogo de materiales de una empresa de construcción, demostrando la diferencia cualitativa entre una IA genérica y una IA entrenada.

**Uso del programa (1)**
El programa `entrenamiento.py` ofrece un menú interactivo con tres opciones. La primera opción realiza el entrenamiento: lee el archivo `training_data.json` con los pares de pregunta-respuesta, genera un `Modelfile` de Ollama y ejecuta el comando `ollama create` para construir un nuevo modelo personalizado llamado `asistente-maderas`. Este proceso tarda aproximadamente un minuto y solo hay que realizarlo una vez.

**Uso del programa (2)**
La segunda opción lanza la demostración "antes y después": el sistema hace la misma pregunta dos veces, primero al modelo base `llama3` y luego al modelo entrenado `asistente-maderas`. La diferencia es notable: el modelo genérico responde con información generalista sobre maderas en todo el mundo, mientras que el modelo entrenado responde específicamente con los datos del catálogo de la empresa, sus precios y sus características concretas.

**Tecnologías (1)**
El proceso de entrenamiento se basa en el concepto de **Modelfile de Ollama**, un fichero de configuración que permite crear modelos derivados añadiendo un prompt de sistema personalizado. Este prompt incluye el rol del asistente y todos los pares de pregunta-respuesta del archivo JSON como ejemplos de few-shot learning. El archivo `training_data.json` contiene 6 pares de entrenamiento que cubren las consultas más frecuentes sobre el catálogo.

**Tecnologías (2)**
La técnica empleada es una combinación de **in-context learning** y **system prompting**: en lugar de modificar los pesos del modelo (fine-tuning clásico que requiere GPU potente), se inyecta el conocimiento específico en el prompt de sistema. Esto es posible gracias a la API de Ollama y al módulo `subprocess` de Python para ejecutar comandos del sistema. El resultado es un modelo que, para el contexto empresarial, se comporta como si hubiera sido entrenado con los datos de la empresa.

**Cierre**
Este proyecto me ha permitido comprender la diferencia entre un modelo de IA genérico y uno especializado, y cómo el system prompting puede sustituir al fine-tuning clásico en muchos casos reales. He aprendido a estructurar datos de entrenamiento en JSON y a generar Modelfiles de Ollama de forma programática. Como mejora, ampliaría el conjunto de pares de entrenamiento a más de 50 ejemplos y exploraría técnicas de fine-tuning real con herramientas como Unsloth, que permiten ajustar los pesos del modelo con hardware modesto.

---

### 3. MCP — MiniSaaS (Model Context Protocol)

**Introducción**
Este proyecto implementa el concepto de Model Context Protocol (MCP), un paradigma que permite a los modelos de inteligencia artificial conectarse e interactuar con aplicaciones externas de forma estructurada. Se ha desarrollado un MiniSaaS que actúa como intermediario entre el usuario y una base de datos empresarial: la IA recibe preguntas en lenguaje humano, las transforma en peticiones de API, obtiene los datos del sistema y los devuelve interpretados en lenguaje natural.

**Uso del programa (1)**
Al ejecutar `python mcp_saas.py`, el usuario accede a un sistema de consulta en lenguaje natural. Puede escribir preguntas como "¿Cuál es el material más barato?" o "Necesito materiales que no cuesten más de 15 euros". El sistema muestra el proceso en tres fases visibles: primero la petición JSON generada por la IA, luego los datos brutos devueltos por el SaaS, y finalmente la respuesta interpretada en lenguaje natural.

**Uso del programa (2)**
El flujo completo es transparente para el usuario pero técnicamente complejo: la pregunta "¿Hay maderas resistentes con buen precio?" se transforma en `{"accion": "filtrar_densidad", "min_densidad": 0.7}`, el SaaS devuelve los registros que cumplen ese criterio, y la IA interpreta esos datos con una respuesta como "Sí, la Madera B tiene una densidad de 0.8 g/cm³ y un precio de 25 unidades, siendo una excelente opción para aplicaciones que requieran resistencia". Todo en segundos.

**Tecnologías (1)**
La arquitectura MCP separa claramente tres componentes. El primero es el **traductor IA**, implementado con Ollama (LLaMA 3), que transforma lenguaje natural en JSON estructurado mediante un prompt de sistema especializado. El segundo es el **SaaS endpoint**, una función Python que simula una API empresarial con operaciones como `listar`, `buscar_por_nombre`, `filtrar_precio` o `mas_barato`. El tercero es el **intérprete IA**, que convierte los datos crudos del SaaS en texto comprensible.

**Tecnologías (2)**
El patrón de diseño implementado es **natural language to API** (NL2API): el modelo de IA actúa como parser semántico que entiende la intención del usuario y la mapea a una acción concreta de la API. Se utiliza **Pandas** para la gestión de datos del catálogo (archivo CSV) y la librería `requests` de Python para la comunicación con Ollama. El sistema extrae el JSON generado por la IA mediante procesamiento de cadenas, siendo robusto ante variaciones en el formato de respuesta del modelo.

**Cierre**
Con este proyecto he aprendido a diseñar arquitecturas donde la IA actúa como capa de traducción entre el lenguaje humano y los sistemas informáticos. He entendido el concepto de MCP y cómo el prompting estructurado puede convertir un LLM en un parser semántico fiable. Como mejora, conectaría el sistema a una API REST externa real (por ejemplo, un ERP o un sistema de inventario en la nube) y añadiría validación del JSON generado por la IA para manejar respuestas malformadas con mayor robustez.

---

### 4. IA Agéntica

**Introducción**
Este proyecto presenta un sistema de inteligencia artificial agéntica: una IA que, a diferencia de los chatbots conversacionales tradicionales, actúa de forma autónoma e independiente para cumplir misiones complejas. Dado un objetivo, el agente decide por sí mismo qué pasos dar, qué herramientas usar y cuándo ha recopilado suficiente información para elaborar un informe final, sin intervención humana durante el proceso.

**Uso del programa (1)**
Al iniciar `python agente_autonomo.py`, el usuario selecciona una misión del menú o escribe una personalizada, por ejemplo: "Encuentra el material más rentable en términos de resistencia por unidad de coste". A partir de ese momento, el agente trabaja de forma autónoma, mostrando en pantalla cada paso que da: qué herramienta decide usar, qué resultado obtiene y cómo ese resultado influye en su siguiente decisión.

**Uso del programa (2)**
El agente itera hasta un máximo de 6 pasos. En cada iteración, el modelo LLM analiza el contexto acumulado y decide si necesita más datos (indicando qué herramienta usar con notación `[nombre_herramienta]`) o si ya tiene suficiente información para elaborar el informe final (indicando `[FINALIZAR]`). El resultado es un informe detallado y justificado que el usuario recibe sin haber intervenido en ningún paso intermedio.

**Tecnologías (1)**
La arquitectura del agente implementa el patrón **ReAct** (Reasoning + Acting): el modelo LLM alterna entre razonar sobre qué hacer y ejecutar acciones concretas. Las herramientas disponibles son funciones Python que acceden al catálogo de materiales (CSV): `listar_materiales`, `material_mas_caro`, `material_mas_barato`, `material_mas_resistente` y `calcular_relacion_calidad_precio`. La IA elige qué herramientas usar y en qué orden.

**Tecnologías (2)**
El sistema utiliza la **API de chat de Ollama** con el modelo LLaMA 3, que mantiene el contexto entre iteraciones a través de un historial de mensajes. La detección de qué herramienta ha decidido usar el modelo se realiza mediante búsqueda de patrones `[nombre_herramienta]` en el texto generado. **Pandas** gestiona los datos del CSV y la lógica de cálculo de métricas como la relación calidad/precio. El bucle de agencia está controlado en Python con un límite de seguridad para evitar loops infinitos.

**Cierre**
Este proyecto me ha enseñado que la diferencia entre un chatbot y un agente autónomo reside en el bucle de razonamiento y el acceso a herramientas externas. He aprendido a implementar el patrón ReAct y a controlar el flujo del agente para que no entre en bucles infinitos. Como mejora, añadiría herramientas más potentes (acceso a internet, escritura de ficheros, envío de emails) y usaría frameworks especializados como LangGraph o CrewAI, que ofrecen una arquitectura más robusta para agentes complejos con múltiples herramientas paralelas.

---

## PROGRAMACIÓN DE SERVICIOS Y PROCESOS

---

### 5. RAG con ChromaDB

**Introducción**
Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) real y completo. A diferencia de los sistemas de búsqueda por palabras clave, el RAG utiliza embeddings semánticos para encontrar la información más relevante en un corpus de texto. El sistema divide documentos en fragmentos (chunks), genera representaciones vectoriales de cada uno y los almacena en ChromaDB, una base de datos vectorial, permitiendo consultas semánticas altamente precisas.

**Uso del programa (1)**
El flujo comienza ejecutando `python rag_real.py`. Si la base de datos no existe, el sistema lee el archivo `corpus.txt`, lo divide en párrafos y los indexa automáticamente en ChromaDB. Si ya existe, pregunta si se desea reinicializar. Una vez lista la base de datos, el usuario puede escribir cualquier pregunta: el sistema devuelve los 3 chunks más semánticamente similares con su porcentaje de similitud, aunque el texto de la pregunta no comparta palabras exactas con los documentos.

**Uso del programa (2)**
La potencia del sistema se observa con preguntas indirectas: si el usuario escribe "madera buena para lluvia", el sistema recupera correctamente el chunk sobre la teca ("resistente al agua y a la intemperie") aunque esas palabras exactas no aparezcan en la pregunta. Esto es la búsqueda semántica: el sistema entiende el significado, no solo las palabras. Los resultados se muestran ordenados por porcentaje de similitud, del más relevante al menos relevante.

**Tecnologías (1)**
El núcleo del sistema es **ChromaDB**, una base de datos vectorial de código abierto diseñada específicamente para almacenar y consultar embeddings. ChromaDB incluye su propia función de embedding basada en modelos ONNX optimizados, lo que elimina la necesidad de instalar librerías adicionales de machine learning. Los vectores se persisten en disco mediante `chromadb.PersistentClient`, lo que significa que la base de datos no se pierde al cerrar el programa.

**Tecnologías (2)**
El algoritmo de búsqueda utilizado por ChromaDB es **HNSW** (Hierarchical Navigable Small World), un índice aproximado de vecinos más cercanos (ANN) que permite búsquedas ultrarrápidas en espacios de alta dimensionalidad. La métrica de distancia es coseno, que mide el ángulo entre vectores independientemente de su magnitud. El corpus de texto se divide en párrafos semánticos en lugar de chunks de tamaño fijo, preservando la coherencia semántica de cada fragmento.

**Cierre**
Con este proyecto he comprendido en profundidad qué son los embeddings y cómo ChromaDB los almacena y consulta mediante índices vectoriales. He aprendido que la búsqueda semántica no depende de las palabras exactas sino del significado, lo cual es un cambio de paradigma fundamental respecto a los buscadores tradicionales. Como mejora, utilizaría un modelo de embeddings multilingüe (como `paraphrase-multilingual-MiniLM-L12-v2`) para obtener mejores resultados en español, y añadiría metadatos a los chunks para filtrar por fecha o categoría.

---

### 6. RAG + IA

**Introducción**
Este proyecto extiende el sistema RAG básico añadiendo una capa de inteligencia artificial que transforma los fragmentos de texto recuperados (chunks crudos) en respuestas comprensibles para cualquier usuario. El RAG por sí solo devuelve información fragmentada y técnica; al combinarlos con un modelo LLM, el sistema genera respuestas coherentes, contextualizadas y adaptadas al nivel del usuario final, cerrando así el ciclo completo de un sistema de respuesta a preguntas.

**Uso del programa (1)**
El programa `rag_ia.py` presenta el proceso en dos fases visibles. Primero muestra los chunks recuperados de ChromaDB, con sus primeros 100 caracteres, para que el usuario comprenda qué información bruta ha encontrado el sistema. A continuación, esos chunks se envían a Ollama como contexto y el modelo genera una respuesta natural. El usuario ve ambas fases, lo que permite comparar los datos crudos con la respuesta elaborada.

**Uso del programa (2)**
La diferencia entre el RAG puro y el RAG con IA es inmediata en la práctica. Ante la pregunta "¿Qué madera uso para hacer una mesa de jardín?", el RAG devuelve fragmentos de texto sobre la teca, el cedro y sus propiedades. La IA toma esos fragmentos y responde: "Para una mesa de jardín te recomiendo la teca, ya que es resistente al agua y a la intemperie de forma natural. También puedes considerar el cedro, que es más económico aunque necesita tratamiento periódico". Una respuesta humana, directa y útil.

**Tecnologías (1)**
El sistema combina **ChromaDB** para la recuperación semántica de chunks con **Ollama (LLaMA 3)** para la generación de lenguaje natural. La clave es el **prompt de sistema**: se construye dinámicamente concatenando los chunks recuperados como contexto y la pregunta del usuario. El modelo recibe instrucciones explícitas de usar únicamente la información del contexto, lo que evita que "alucine" datos no presentes en el corpus.

**Tecnologías (2)**
La técnica de prompting empleada es **RAG prompting** o **grounded generation**: el LLM está anclado a un contexto específico y no puede inventar información. El parámetro `n_resultados=3` en la consulta a ChromaDB equilibra la cantidad de contexto (más contexto = respuestas más completas) con el límite de tokens del modelo. La comunicación con Ollama usa `requests.post` con un timeout de 60 segundos para gestionar correctamente los tiempos de generación variables.

**Cierre**
Este proyecto me ha hecho entender por qué RAG + IA es la arquitectura dominante en aplicaciones empresariales de IA: resuelve tanto el problema de la alucinación (el modelo solo usa el contexto proporcionado) como el de la información desactualizada (el corpus se puede actualizar sin reentrenar el modelo). Como mejora, implementaría streaming de la respuesta para que el texto aparezca palabra a palabra en lugar de esperar al final, mejorando considerablemente la experiencia de usuario.

---

### 7. RAG Empaquetado (Flask)

**Introducción**
Este proyecto encapsula todo el sistema RAG en una interfaz web desarrollada con Flask, haciendo que cualquier usuario sin conocimientos técnicos pueda entrenar su propio sistema de búsqueda semántica y consultarlo. La aplicación guía al usuario en cuatro pasos visuales: subir el texto, indexación automática en ChromaDB, búsqueda semántica y respuesta de la IA, todo desde un navegador web sin necesidad de instalar nada ni abrir una terminal.

**Uso del programa (1)**
El usuario accede a la aplicación en `http://localhost:5000` tras ejecutar `python app_flask.py`. En la sección "Entrenar el RAG", pega el texto que quiere que la IA aprenda (puede ser un manual, un artículo, documentación técnica o cualquier texto) y pulsa "Entrenar RAG". El sistema divide automáticamente el texto en chunks, genera los embeddings y los almacena en ChromaDB, mostrando cuántos fragmentos han sido indexados.

**Uso del programa (2)**
Una vez entrenado, el usuario escribe su pregunta en el campo de búsqueda y pulsa Enter o el botón "Buscar". La interfaz muestra dos resultados en tiempo real: primero los chunks más similares con su porcentaje de similitud semántica (datos crudos del RAG), y acto seguido la respuesta generada por la IA que interpreta esos chunks en lenguaje natural. Todo el proceso ocurre en segundos y sin recargar la página gracias a las peticiones AJAX.

**Tecnologías (1)**
La aplicación está desarrollada con **Flask**, el framework web ligero de Python. La interfaz de usuario está construida con HTML, CSS y JavaScript vanilla (sin frameworks), con un diseño oscuro y moderno que proporciona una experiencia de usuario fluida. Cada sesión de usuario recibe un identificador único (`session_id`) que aísla su colección en ChromaDB, permitiendo que múltiples usuarios entrenen sus propios RAGs de forma independiente en el mismo servidor.

**Tecnologías (2)**
La comunicación entre el frontend y el backend se realiza mediante tres endpoints REST: `/train` (POST, indexa el texto), `/query` (POST, realiza la búsqueda semántica en ChromaDB) y `/generate` (POST, llama a Ollama para generar la respuesta). Este diseño desacoplado permite que la interfaz muestre los chunks antes de que la IA termine de responder, ofreciendo feedback visual inmediato al usuario. **ChromaDB PersistentClient** garantiza que los datos sobreviven a reinicios del servidor.

**Cierre**
Este proyecto me ha enseñado a integrar múltiples tecnologías (Flask, ChromaDB, Ollama) en una sola aplicación web cohesiva con comunicación asíncrona entre frontend y backend. He aprendido a gestionar sesiones de usuario independientes en una base de datos compartida. Como mejora, añadiría autenticación de usuarios, la posibilidad de subir archivos PDF directamente (con extracción de texto automática mediante PyMuPDF) y un panel de administración para gestionar las colecciones almacenadas en ChromaDB.

---

### 8. CSS 3D

**Introducción**
Este proyecto explora las capacidades de CSS3D, la especificación CSS que permite crear entornos y transformaciones tridimensionales directamente en el navegador sin necesidad de librerías externas. Se ha desarrollado una visualización interactiva del pipeline RAG (Retrieval-Augmented Generation) en un espacio 3D, combinando transformaciones CSS con animaciones y un buscador semántico funcional, relacionando así el contenido visual con los conceptos de IA trabajados en los demás proyectos.

**Uso del programa (1)**
El archivo `css3d.html` se abre directamente en cualquier navegador moderno (doble clic o arrastrar al navegador). El usuario observa una escena 3D animada que muestra el pipeline completo del RAG: a la izquierda, los chunks de texto con su porcentaje de similitud; en el centro, un cubo 3D rotatorio que representa la base de datos ChromaDB; y a la derecha, los bloques de entrada y salida de la IA. El cubo se puede pausar pasando el ratón por encima.

**Uso del programa (2)**
En la parte inferior de la página hay un buscador interactivo: el usuario escribe una pregunta y el sistema muestra instantáneamente los chunks más relevantes de una base de conocimiento local, con su porcentaje de similitud semántica. A continuación aparece la respuesta generada por la IA (simulada en el HTML para funcionar sin servidor). Esta sección demuestra de forma visual cómo funciona la búsqueda semántica en el contexto del RAG explicado en otros proyectos.

**Tecnologías (1)**
La técnica central es **CSS 3D Transforms**: la propiedad `transform-style: preserve-3d` crea un contexto de renderizado tridimensional, y las propiedades `rotateX`, `rotateY`, `translateZ` posicionan las caras del cubo en el espacio 3D. La propiedad `perspective` en el contenedor padre controla la profundidad de campo de la escena. Las animaciones se definen con `@keyframes` y se aplican con la propiedad `animation`, sin ningún JavaScript para las transformaciones 3D.

**Tecnologías (2)**
Los efectos visuales incluyen **partículas de fondo** generadas dinámicamente con JavaScript (30 elementos con posición, duración y delay aleatorios), animaciones de **flotación** con `translateY` para los chunks, y transiciones CSS para los efectos hover. El diseño sigue una paleta de colores oscura con acentos en azul cyan (`#38bdf8`, `#0ea5e9`), inspirada en las herramientas de visualización de datos modernas. Todo el proyecto es un único archivo HTML autocontenido, sin dependencias externas.

**Cierre**
Con este proyecto he aprendido a dominar `transform-style: preserve-3d`, `perspective` y `translateZ` para crear escenas tridimensionales reales en el navegador sin librerías externas. También he entendido cómo combinar CSS puro con JavaScript para añadir interactividad. Como mejora, conectaría el buscador interactivo directamente a la API Flask del RAG empaquetado mediante fetch, de modo que las respuestas sean reales en lugar de simuladas, creando una demo completamente funcional del pipeline RAG dentro de un entorno 3D.

---
*Todos los proyectos utilizan Python 3, Ollama (LLaMA 3) y ChromaDB.*
*Comandos de ejecución: ver README de cada archivo.*
