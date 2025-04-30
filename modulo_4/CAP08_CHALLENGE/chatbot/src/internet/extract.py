# src/internet/extract.py
import logging
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
# Quitar requests y BeautifulSoup si newspaper los maneja internamente
# import requests
# from bs4 import BeautifulSoup
from newspaper import Article, ArticleException # Usar newspaper4k

log = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    """Verifica si una URL tiene un esquema y un netloc válidos."""
    if not isinstance(url, str): return False
    try:
        result = urlparse(url)
        # Permitir http y https
        return result.scheme in ['http', 'https'] and bool(result.netloc)
    except ValueError:
        return False

def extract_text_from_url_newspaper(url: str, language: str = 'es', timeout: int = 15) -> Optional[str]:
    """
    Extrae el texto principal de una URL dada usando newspaper4k.

    Args:
        url: La URL de la página web.
        language: Código de idioma ISO 639-1 (ej. 'es', 'en') para ayudar a newspaper.
        timeout: Tiempo máximo de espera para la solicitud HTTP subyacente.

    Returns:
        El texto del artículo extraído o None si ocurre un error.
    """
    if not is_valid_url(url):
        log.warning(f"URL inválida o no soportada para extracción: {url}")
        return None

    log.debug(f"Intentando extraer texto de: {url} (Idioma: {language}, Timeout: {timeout}s)")
    try:
        # Configurar el artículo
        article = Article(url, language=language, fetch_images=False, request_timeout=timeout)
        # Descargar el contenido HTML
        article.download()
        # Parsear el contenido para extraer información
        article.parse()

        # --- Verificaciones adicionales ---
        # Comprobar si se pudo parsear correctamente (a veces parsea pero no extrae texto)
        if not article.is_parsed:
             log.warning(f"Newspaper no pudo parsear contenido útil de: {url}")
             return None

        # Extraer el texto principal
        extracted_text = article.text

        # Verificar si el texto extraído es significativo
        if not extracted_text or len(extracted_text.strip()) < 100: # Umbral mínimo de caracteres
            log.warning(f"Texto extraído de {url} es demasiado corto o vacío después del parseo.")
            # A veces el título es útil si el texto falla
            if article.title and len(article.title) > 20:
                 log.info(f"Usando título como fallback para {url}: '{article.title}'")
                 return f"Título: {article.title}" # Devolver solo el título como fallback
            return None

        log.debug(f"Texto extraído de {url} (primeros 100 chars): {extracted_text[:100]}...")

        # Limitar la longitud para no sobrecargar al LLM (opcional pero recomendado)
        max_len = 4000 # Ajustar según necesidad
        final_text = extracted_text.strip() # Quitar espacios al inicio/fin
        if len(final_text) > max_len:
            log.info(f"Texto de {url} truncado a {max_len} caracteres.")
            return final_text[:max_len] + "..."
        else:
            return final_text

    except ArticleException as e:
        # Errores específicos de Newspaper (ej. 404, fallo de descarga)
        log.error(f"Newspaper ArticleException al procesar {url}: {e}")
        return None
    except Exception as e:
        # Captura errores inesperados durante el proceso de newspaper
        log.exception(f"Error inesperado al procesar {url} con Newspaper:")
        return None

def extract_content_from_links(links: List[str], language: str = 'es') -> Dict[str, str]:
    """
    Extrae texto de una lista de URLs usando newspaper4k.

    Args:
        links: Lista de URLs a procesar.
        language: Código de idioma para newspaper.

    Returns:
        Un diccionario donde las claves son las URLs válidas y procesadas
        y los valores son el texto extraído. URLs fallidas no se incluyen.
    """
    extracted_data = {}
    if not links:
        return {}

    log.info(f"Iniciando extracción de contenido para {len(links)} links...")
    from src.streaming.streamer import stream_message # Importación local
    stream_message("\n** Extrayendo contenido de las fuentes... **")

    processed_count = 0
    success_count = 0
    for url in links:
        processed_count += 1
        # Usar la nueva función de extracción
        content = extract_text_from_url_newspaper(url, language=language)
        if content:
            extracted_data[url] = content
            success_count += 1
            log.debug(f"({processed_count}/{len(links)}) Éxito extrayendo de: {url}")
        else:
            # El log de error/warning ya se hizo dentro de extract_text_from_url_newspaper
            log.warning(f"({processed_count}/{len(links)}) Falló la extracción para: {url}")

    log.info(f"Extracción completada. {success_count} de {len(links)} links procesados exitosamente.")
    stream_message("** Extracción completada. **")
    return extracted_data

# Mantener la función anterior con BeautifulSoup por si se quiere comparar o usar como fallback
# (Renombrada para evitar colisión)
# def extract_text_from_url_bs(url: str, timeout: int = 10) -> Optional[str]: ... (código anterior)