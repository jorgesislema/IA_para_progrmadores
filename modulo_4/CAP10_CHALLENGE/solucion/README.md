# Sistema de Atención al Cliente Automatizado con LangChain

Este proyecto implementa un sistema de atención al cliente automatizado utilizando LangChain, capaz de procesar solicitudes de clientes y decidir el método más apropiado para responder, ya sea consultando una base de datos, una base de conocimientos, o utilizando el conocimiento integrado en un modelo de lenguaje de gran escala (LLM).

## Descripción del Sistema

El sistema automatizado de atención al cliente implementa tres flujos de trabajo principales:

1. **Consulta de Balance de Cuentas:** Extrae información de un archivo CSV basado en un ID específico proporcionado por el usuario.
   
2. **Información General sobre Procesos Bancarios:** Recupera y genera respuestas a partir de una base de conocimientos sobre procedimientos bancarios específicos como abrir cuentas o realizar transferencias.

3. **Consultas Generales:** Utiliza el conocimiento incorporado en el modelo de lenguaje para responder a preguntas que no requieren consultar bases de datos o conocimientos específicos.

## Modelos de Lenguaje Soportados

El sistema ahora soporta múltiples proveedores de modelos de lenguaje:

1. **OpenAI (GPT)**: Los tradicionales modelos GPT de OpenAI.
   - Requiere clave API de OpenAI

2. **Google (Gemini)**: Modelos Gemini de Google.
   - Requiere clave API de Google AI

3. **Mistral AI**: Modelos de Mistral.
   - Requiere clave API de Mistral

4. **Groq**: Plataforma especializada en alta velocidad de inferencia.
   - Requiere clave API de Groq

Al iniciar el sistema, se mostrará un menú para seleccionar el modelo a utilizar.

3. **Respuestas Generales:** Utiliza el conocimiento del LLM para responder preguntas generales que no requieren consulta de datos externos.

## Estructura del Proyecto

```
solucion/
│
├── main.py                # Script principal que implementa el sistema de atención al cliente
├── indexer.py             # Script para indexar la base de conocimientos
├── test_system.py         # Pruebas automatizadas del sistema
├── config_api.py          # Configuración de claves API para diferentes modelos
│
└── index/                 # Directorio donde se almacena el índice FAISS (generado por indexer.py)
    └── ...

knowledge_base/            # Base de conocimientos con información sobre procesos bancarios
├── nueva_cuenta.txt
├── tarjeta_credito.txt
└── transferencia.txt

saldos.csv                 # Archivo CSV con información de balances de clientes
```

## Tecnologías Utilizadas

- **LangChain:** Framework para desarrollo de aplicaciones basadas en modelos de lenguaje.
- **FAISS:** Biblioteca para búsqueda eficiente de similitud y agrupación de vectores densos.
- **Sentence Transformers:** Biblioteca para generar embeddings de alta calidad.
- **Multiple LLM Providers:** Integración con OpenAI, Google, Mistral y Groq.

## Requisitos

- Python 3.8 o superior
- Dependencias especificadas en `requirements.txt`
- Clave API para al menos uno de los proveedores de LLM soportados

## Instalación

1. Clona este repositorio o descárgalo

2. Crea un entorno virtual (recomendado):

```bash
python -m venv venv
```

3. Activa el entorno virtual:

```bash
# En Windows
venv\Scripts\activate

# En Unix o MacOS
source venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

5. Configura tus claves API en el archivo `config_api.py` o permite que el sistema te las solicite durante la ejecución:

```python
# config_api.py
API_KEYS = {
    "openai": "sk-...",  # OpenAI (GPT)
    "google": "...",     # Google (Gemini)
    "mistral": "...",    # Mistral AI
    "groq": "..."        # Groq
}
```

## Uso

### Indexación de la Base de Conocimientos

Antes de ejecutar el sistema por primera vez, o después de realizar cambios en la base de conocimientos, debes ejecutar el script de indexación:

```bash
cd solucion
python indexer.py
```

Este script generará un índice FAISS en el directorio `index/` basado en el contenido de la carpeta `knowledge_base/`.

### Ejecución del Sistema

Para iniciar el sistema de atención al cliente:

```bash
cd solucion
python main.py
```

Al iniciar el sistema, se mostrará un menú para seleccionar el modelo LLM a utilizar:

```bash
cd solucion
python main.py
```

Al iniciar el sistema, se mostrará un menú para seleccionar el modelo LLM a utilizar:

```
=== Selección de Modelo de Lenguaje ===
Seleccione el modelo de IA que desea utilizar:
1. OpenAI (GPT) (✓ Instalado)
2. Google (Gemini) (✓ Instalado)
3. Mistral AI (✓ Instalado)
4. Groq (✓ Instalado)

Ingrese el número del modelo (o 'q' para salir):
```

Una vez seleccionado el modelo, podrás interactuar con el sistema mediante consultas en lenguaje natural.

El sistema procesará tus consultas según corresponda:
- Para consultas de balance, incluye un ID de cédula en tu pregunta.
- Para información sobre procesos bancarios, pregunta sobre cómo abrir cuentas, solicitar tarjetas, etc.
- Para consultas generales, simplemente realiza tu pregunta.

Para salir del sistema, escribe "salir".

### Ejecución de Pruebas

Para ejecutar las pruebas automatizadas del sistema:

```bash
cd solucion
python test_system.py
```

## Pruebas y Verificación

Para verificar el correcto funcionamiento del sistema:

1. El sistema ahora permite seleccionar entre diferentes modelos LLM.
2. La función `select_model()` muestra los modelos disponibles y permite al usuario elegir.
3. La clase `CustomerSupportSystem` ha sido actualizada para aceptar cualquier modelo LLM.
4. Las pruebas automatizadas (`test_system.py`) han sido actualizadas para ser compatibles con la nueva implementación.

**Importante**: Para utilizar cualquiera de los modelos, es necesario disponer de una clave API válida. Si no se dispone de una clave API, se producirá un error al procesar las consultas.

3. **Procesador de Consultas de Conocimiento:**
   - Utiliza embeddings y FAISS para encontrar información relevante en la base de conocimientos.
   - Genera respuestas basadas en la información recuperada.

4. **Procesador de Consultas Generales:**
   - Utiliza el LLM directamente para responder preguntas generales.

### Flujo de Trabajo

1. El usuario ingresa una consulta.
2. El router analiza la consulta y determina el flujo adecuado.
3. La consulta se procesa según el flujo seleccionado.
4. La respuesta generada se presenta al usuario.

## Mejoras Futuras

- Implementación de una interfaz web o API REST.
- Soporte para más idiomas.
- Integración con sistemas CRM existentes.
- Mejora de la precisión del router mediante fine-tuning.
- Implementación de feedback del usuario para mejorar el sistema.
