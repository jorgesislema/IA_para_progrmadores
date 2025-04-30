#librerias
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Verificamos si una URL tiene un esquema y un netloc válidos."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_text_from_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    Extraemos el texto principal de una URL dada.

    Args:
        url: La URL de la página web.
        timeout: Tiempo máximo de espera para la solicitud HTTP.

    Returns:
        El texto extraído o None si ocurre un error o el contenido no es adecuado.
    """
    if not is_valid_url(url):
        print(f"URL inválida o incompleta: {url}")
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status() # Lanza excepción para errores HTTP

        # Verificar si el contenido es HTML
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' not in content_type:
            print(f"Contenido no es HTML para {url} (Tipo: {content_type}). Saltando.")
            return None

        # Usamos encoding detectado por requests si está disponible, sino UTF-8
        response.encoding = response.apparent_encoding or 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        # Eliminamos elementos no deseados (scripts, styles, nav, footers)
        for element in soup(["script", "style", "nav", "footer", "aside", "form", "header"]):
            element.decompose()

        # Extraemos texto de etiquetas comunes de contenido
        main_content = soup.find('article') or soup.find('main') or soup.body
        if not main_content:
             # Si no hay body (extraño), intentar con todo el soup
            main_content = soup

        text_parts = main_content.find_all(string=True, recursive=True)

        # Filtramos y limpiamos el texto
        visible_text = ""
        for part in text_parts:
            stripped = part.strip()
            # Evitar texto vacío, comentarios, o texto dentro de etiquetas eliminadas indirectamente
            if stripped and not part.parent.name in ["script", "style", "meta", "[document]"]:
                 # Añadir espacio entre elementos para mejor legibilidad
                visible_text += stripped + " "

        # Limpiamos espacios múltiples y saltos de línea excesivos
        cleaned_text = ' '.join(visible_text.split())

        # Devolver None si el texto es demasiado corto (probablemente no útil)
        if len(cleaned_text) < 100:
            print(f"Texto extraído de {url} es muy corto. Saltando.")
            return None

        # Limitamos la longitud para no sobrecargar al LLM (opcional)
        max_len = 5000 # Caracteres
        return cleaned_text[:max_len] + ("..." if len(cleaned_text) > max_len else "")


    except requests.exceptions.Timeout:
        print(f"Timeout al intentar acceder a {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP {e.response.status_code} al acceder a {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al acceder a {url}: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar {url}: {e}")
        return None


def extract_content_from_links(links: List[str]) -> Dict[str, str]:
    """
    Extrae texto de una lista de URLs.

    Args:
        links: Lista de URLs a procesar.

    Returns:
        Un diccionario donde las claves son las URLs y los valores son
        el texto extraído (o un mensaje de error si falló).
    """
    extracted_data = {}
    if not links:
        return {}

    print("\n** Extrayendo contenido de las fuentes... **")
    for url in links:
        print(f" - Procesando: {url}")
        content = extract_text_from_url(url)
        if content:
            extracted_data[url] = content
        else:
            # Podríamos decidir no incluir URLs fallidas o incluir un marcador
            # extracted_data[url] = "Error: No se pudo extraer contenido."
            print(f"   -> No se pudo extraer contenido útil de {url}")

    print("** Extracción completada. **")
    return extracted_data