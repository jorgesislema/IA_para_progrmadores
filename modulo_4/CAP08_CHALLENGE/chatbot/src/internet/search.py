#librerias
import os
import requests
import json
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Cargarmos las variables de entorno desde .env al inicio
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_google(query: str, num_results: int = 5) -> Optional[List[Dict[str, Any]]]:
    """
    Realizamos una búsqueda en Google utilizando la API de Serper.dev.

    Args:
        query: La consulta de búsqueda del usuario.
        num_results: El número máximo de resultados a devolver.

    Returns:
        Una lista de diccionarios con los resultados orgánicos (título, enlace, snippet),
        o None si ocurre un error o no se encuentra la API key.
    """
    if not SERPER_API_KEY:
        print("Error: La variable de entorno SERPER_API_KEY no está configurada.")
        return None

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": num_results})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    print(f"\n** Buscando en internet sobre: '{query}' ... **") # Mensaje indicador

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()  # Lanza excepción para errores HTTP (4xx o 5xx)

        search_results = response.json()

        # Extraer los resultados orgánicos principales
        organic_results = search_results.get('organic', [])

        if not organic_results:
            print("No se encontraron resultados orgánicos en la búsqueda.")
            return []

        # Devolver solo la información relevante (título, link, snippet)
        relevant_results = [
            {
                "title": r.get("title", "Sin título"),
                "link": r.get("link", ""),
                "snippet": r.get("snippet", "")
            }
            for r in organic_results if r.get("link") # Asegurarse que hay un link
        ][:num_results] # Limitar al número deseado

        return relevant_results

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Serper.dev: {e}")
        return None
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON de Serper.dev.")
        return None
    except Exception as e:
        print(f"Error inesperado durante la búsqueda: {e}")
        return None

# --- Esquema para Function Calling (Ejemplo) ---
# Este es un ejemplo de cómo podrías definir la función para un LLM
# que soporte function calling (como los modelos de OpenAI o Gemini).
# La estructura exacta puede variar según el LLM.
SEARCH_FUNCTION_SCHEMA = {
    "name": "buscar_en_google",
    "description": "Realiza una búsqueda en Google para obtener información actualizada o específica.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "La consulta de búsqueda detallada para Google.",
            }
        },
        "required": ["query"],
    },
}