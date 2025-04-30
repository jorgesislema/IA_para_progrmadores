# src/internet/search.py
import os
import requests
import json
import logging
from typing import List, Optional, Dict, Any
# La carga de dotenv se hace ahora en main.py antes de importar
# from dotenv import load_dotenv
# load_dotenv()

log = logging.getLogger(__name__)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_google(query: str, num_results: int = 5) -> Optional[List[Dict[str, Any]]]:
    """
    Realiza una búsqueda en Google utilizando la API de Serper.dev.

    Args:
        query: La consulta de búsqueda del usuario.
        num_results: El número máximo de resultados a devolver.

    Returns:
        Una lista de diccionarios con los resultados orgánicos (título, enlace, snippet),
        o None si ocurre un error o no se encuentra la API key.
    """
    if not SERPER_API_KEY:
        log.error("SERPER_API_KEY no está configurada en las variables de entorno.")
        # Considerar lanzar una excepción aquí en lugar de devolver None
        # raise ValueError("SERPER_API_KEY no configurada.")
        return None

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": num_results})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    log.info(f"Realizando búsqueda en Serper para: '{query}' (num_results={num_results})")
    # Usar stream_message para indicar al usuario en consola que se está buscando
    from src.streaming.streamer import stream_message # Importación local o pasar como argumento
    stream_message(f"\n** Buscando en internet sobre: '{query}' ... **")

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=15) # Timeout un poco más largo
        response.raise_for_status()  # Lanza excepción para errores HTTP (4xx o 5xx)

        search_results = response.json()
        log.debug(f"Respuesta JSON cruda de Serper: {search_results}") # Log detallado (cuidado con datos sensibles si los hubiera)

        # Extraer los resultados orgánicos principales
        organic_results = search_results.get('organic', [])

        if not organic_results:
            log.warning(f"No se encontraron resultados orgánicos en Serper para la consulta: '{query}'")
            return []

        # Devolver solo la información relevante (título, link, snippet)
        relevant_results = []
        for r in organic_results:
            link = r.get("link")
            if link: # Asegurarse que hay un link
                 relevant_results.append({
                    "title": r.get("title", "Sin título"),
                    "link": link,
                    "snippet": r.get("snippet", "")
                 })
            else:
                 log.warning(f"Resultado de Serper omitido por falta de link: {r.get('title')}")

        # Limitar al número deseado después de filtrar
        final_results = relevant_results[:num_results]
        log.info(f"Búsqueda exitosa. Se encontraron {len(final_results)} resultados relevantes.")
        return final_results

    except requests.exceptions.Timeout:
        log.error(f"Timeout al conectar con la API de Serper.dev para la consulta: '{query}'")
        return None
    except requests.exceptions.HTTPError as e:
         log.error(f"Error HTTP {e.response.status_code} de la API de Serper.dev: {e}")
         # Podrías querer inspeccionar e.response.text para más detalles si es JSON
         try:
             error_details = e.response.json()
             log.error(f"Detalles del error de Serper: {error_details}")
         except json.JSONDecodeError:
             log.error(f"Respuesta de error no JSON de Serper: {e.response.text}")
         return None
    except requests.exceptions.RequestException as e:
        log.error(f"Error de conexión/red al contactar con Serper.dev: {e}")
        return None
    except json.JSONDecodeError:
        log.error("Error al decodificar la respuesta JSON de Serper.dev.")
        # Podrías querer loguear response.text aquí si está disponible
        return None
    except Exception as e:
        # Captura genérica para errores inesperados
        log.exception(f"Error inesperado durante la búsqueda en Serper para '{query}':") # Usar log.exception para incluir traceback
        return None

# --- Esquema para Function Calling (sin cambios) ---
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