# LIBRERIAS
import textwrap
from typing import List

def format_response_with_references(response_text: str, references: List[str]) -> str:
    """
    Añadimos una sección de referencias formateada al final de la respuesta del LLM.

    Args:
        response_text: El texto de la respuesta generada por el LLM.
        references: Una lista de URLs usadas como fuentes.

    Returns:
        La cadena de texto completa con la respuesta y las referencias.
    """
    if not references:
        return response_text

    formatted_references = "\n\n---\n**Referencias:**\n"
    for i, url in enumerate(references, 1):
        formatted_references += f"[{i}] {url}\n"

    # Envuelve el texto principal para mejorar la legibilidad en la consola
    wrapped_response = textwrap.fill(response_text.strip(), width=80)

    return wrapped_response + formatted_references